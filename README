<h1 align="center">surface scratcher</h1>

Download images and labels from *[scratch the surface](https://scratchthesurface.tumblr.com/)*.

![scratch-the-surface](https://user-images.githubusercontent.com/25433159/101905119-d6dba800-3bae-11eb-8aa7-e7730865a85a.png)

Scratch the surface is a blog I maintain with a **labeled collection of surfaces**.

Its goals are:

- Highlight the often unnoticed beauty of the surfaces around us.

- Provide an ever increasing repository of labeled surfaces. 

If you wanted a labeled collection of surfaces to train a classifier, to texturize your videogame or because any other reason, you came to the right place. 

# Required libraries

- [BeautifulSoup](https://pypi.org/project/beautifulsoup4/)
- [pandas](https://pypi.org/project/pandas/)
- [requests](https://pypi.org/project/requests/)

# Command line usage

Download images, contexts and labels:

```
python3 surface-scratcher.py
```

I try to upload a new surface everyday, so if you want to keep your local dataset up to date, you can do as follows:

```
python3 surface-scratcher.py --update
```

Each surface has a context image, i.e. a photo of the object that contains said surface. If you don't want/need the context images, you can disable its download:

```
python3 surface-scratcher.py --no_context
```

This information is also available, doing so: `python3 surface-scratcher.py -h`

# Output

After running the program will you get two folders: *surfaces* and *contexts* that contain the surfaces and the context images respectively. Each image is labeled with its index. 

You will also get a csv file named *labels.csv* where each row contains the index and information of each surface.

# License

This program is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
