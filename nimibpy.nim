import std / os
import nimpy
import nimib
import nimib / config
from nimib / themes import nil
from nimib / renders import nil

# using a global object
var nb: NbDoc

proc do_init*(filename: string) {. exportpy .} =
    let theme = themes.useDefault
    let backend = renders.useHtmlBackend
    nb.initDir = getCurrentDir().AbsoluteDir
    # loadOptions nb # skipping for the moment
    loadCfg nb
    nb.thisFile = filename.AbsoluteFile
    echo "[nimibpy] thisFile: ", nb.thisFile
    try:
        nb.source = read(nb.thisFile)
    except IOError:
        echo "[nimibpy] cannot read source"
    
    # no option handling currently
    nb.filename = nb.thisFile.string.splitFile.name & ".html"
    
    if nb.cfg.srcDir != "":
        echo "[nimib] srcDir: ", nb.srcDir
        nb.filename = (nb.thisDir.relativeTo nb.srcDir).string / nb.filename
        echo "[nimib] filename: ", nb.filename

    if nb.cfg.homeDir != "":
        echo "[nimib] setting current directory to nb.homeDir: ", nb.homeDir
        setCurrentDir nb.homeDir

    # can be overriden by theme, but it is better to initialize this anyway
    nb.templateDirs = @["./", "./templates/"]
    nb.partials = initTable[string, string]()
    nb.context = newContext(searchDirs = @[]) # templateDirs and partials added during nbSave

    # apply render backend (default backend can be overriden by theme)
    backend nb

    # apply theme
    theme nb

proc add_block*(command: string, code: string, output: string) =
    let blk = NbBlock(command: command, code: code, output: output, context: newContext(searchDirs = @[], partials = nbDoc.partials))
    nb.blocks.add blk
    nb.blk = blk

proc add_code*(source: string, output: string) {. exportpy .} =
    add_block("nbCode", source, output)
    nb.blk.context["code"] = nb.blk.code
    nb.blk.context["output"] = nb.blk.output

proc add_text*(output: string) {. exportpy .} =
    add_block("nbText", "", output)

proc save*() {. exportpy .} =
    # need to change filename here! and maybe also source!
    nbSave
