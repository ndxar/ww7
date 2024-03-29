userThemeDefault = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>notebook</title>
    <link rel="stylesheet" href="/static/tufte.css" type="text/css">
</head>
<body>
    <h1>Notebook</h1>

    <div id="posts">

        {% for post,meta in posts %}
            <div id="post-{{post.id}}">

                <div id="post-title">
                    <a href="/~{{post.user.username}}/{{meta.url[0]}}">{{ post.creationDate.strftime('%Y-%m-%d') }} &mdash;{{ meta.title[0] }}</a>
                </div>
                <div id="post-date">
                    
                </div>
            </div>
        {% endfor %}

    </div>
</body>
</html>
"""

postThemeDefault = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>meta.title[0]</title>
    <link rel="stylesheet" href="/static/tufte.css" type="text/css">
</head>
<body>
    <div id="post">

            <div id="post-{{post.id}}">

                <div id="post-title">
                    <h1>{{ meta.title[0] }}</h1>
                </div>
                <div id="post-date">
                    {{ post.creationDate.strftime('%a, %B %d, %Y') }}
                </div>
                <hr>

                <div id="post-content">
                    <section>
                        {{post.content}}
                    </section>
                </div>


            </div>

    </div>
</body>
</html>
"""