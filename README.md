# Requirements

python 3

# What does it do?

You list an item you want to build with its components that you will also build yourself.

Your run main.py.

You get the materials list to build the item from the base materials.

If you don't wanna build all the item components, no problem. 

Just list the components you want to build and the ones that you didn't list will be listed for buying on the materials file.

# How do I use it?

- Create a _.mat_ file inside the _materials_ folder
- Paste the blueprint for the item you want to build
- Paste the blueprints for the item's components that you want to build yourself (separated by a line break)
- Run _python main.py_
- Open the file with the same name as the one you created but inside the _materials_ folder
- Copy the contents from the second line down (first line is total time calculated sequentially)
- Open Eve
- Open Menu > Finance > Multibuy
- Click _Import item order_ on the top left
- Click _Add items listed in clipboard to order_

# How do I copy a blueprint into a product file?

- Open Eve
- Open your blueprint
- Go to _industry_ tab on the blueprint
- Collapse the _required skills_ field
- Expand all the other fields
- Press ctrl + a
- Press ctrl + c
- Open your _product file_
- Break a line if it is not the first blueprint on the file
- Press ctrl + v