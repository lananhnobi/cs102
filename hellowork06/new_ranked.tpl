<!DOCTYPE html>
<html>
    <head>
        <link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.12/semantic.min.css"></link>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.12/semantic.min.js"></script>
    </head>
    <body>
        <div class="ui container" style="padding-top: 10px;">
        <a href="/"><< Разметка новостей</a>
        <table class="ui celled table">
            <thead>
                <th>Title</th>
                <th>Author</th>
                <th>#Likes</th>
                <th>#Comments</th>
                <th>Prediction</th>
            </thead>
            <tbody>
                %for row in rows:
                    %if row[0] == 'good':
                    <tr>
                        <td><a href="{{ row[1].url }}">{{ row[1].title }}</a></td>
                        <td>{{ row[1].author }}</td>
                        <td>{{ row[1].points }}</td>
                        <td>{{ row[1].comments }}</td>
                        <td>Интересно</td>
                    </tr>
                    %end
                %end

                %for row in rows:
                    %if row[0] == 'maybe':
                    <tr>
                        <td><a href="{{ row[1].url }}">{{ row[1].title }}</a></td>
                        <td>{{ row[1].author }}</td>
                        <td>{{ row[1].points }}</td>
                        <td>{{ row[1].comments }}</td>
                        <td>Возможно</td>
                    </tr>
                    %end
                %end

                %for row in rows:
                    %if row[0] == 'never':
                    <tr>
                        <td><a href="{{ row[1].url }}">{{ row[1].title }}</a></td>
                        <td>{{ row[1].author }}</td>
                        <td>{{ row[1].points }}</td>
                        <td>{{ row[1].comments }}</td>
                        <td>Не интересно</td>
                    </tr>
                    %end
                %end
            </tbody>
            <tfoot class="full-width">
                <tr>
                    <th colspan="7">
                        <a href="/update" class="ui right floated small primary button">I Wanna more Hacker News!</a>
                    </th>
                </tr>
            </tfoot>
        </table>
        </div>
    </body>
</html>
