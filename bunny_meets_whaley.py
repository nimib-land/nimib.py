import nimib as nb

nb.init(pyscript=True)

nb.text("## Bunny 🐰 meets Whaley 🐳!")
nb.text("Hello world example for pyscript with nimib.py.")

nb.html("<button id=\"click-me\">Click me! 🐰🐳</button><br/>")

nb.text("This code adds functionality to the button (try block is a workaround):")
with nb.code(pyscript=True):
    try:
        from js import document

        def handler(e):
            output = document.createElement("span")
            output.innerHTML = "🐳"
            document.body.appendChild(output)

        button = document.querySelector("button#click-me")
        button.addEventListener("click", handler)
    except ImportError:
        print("running pyscript block not in js")

nb.save()
