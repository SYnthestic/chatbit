from application import app
from flask import render_template, Flask, request, jsonify
import sys
sys.path.append(".")
from aa import ABC
# from chatbotic import get_response
# from chatbot import get_response

#Handles http://127.0.0.1:5000/hello
#Handles http://127.0.0.1:5000/
@app.route('/') 
@app.route('/index') 


@app.route('/login')
def login():
    return render_template("logger.html", title="Log In", index=True )

@app.route('/loggedin')
def welcome():
    return render_template("aboutus.html", title="Welcome!", index=True )

@app.route('/home') 
def homesweethome():
    return render_template("aboutus.html", title="Home, sweet home!", index=True )

@app.route('/logout')
def goodbye():
    return render_template("logger.html", title="Goodbye!", index=True )

@app.route('/chatbottalk')
def chatbottalk():
    return render_template("index.html")

@app.route('/activatechatbot')
def activatechatbot():
    return '''
        <html>
            <head>
                <title>Chatbot Demo</title>
            </head>
            <body>
                <h1>Chatbot Demo</h1>
                <div id="chat-container"></div>
                <form id="chat-form">
                    <input type="text" id="chat-input" name="message">
                    <button type="submit">Send</button>
                </form>
            </body>
            <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
            <script>
                $(document).ready(function() {
                    $('#chat-form').submit(function(e) {
                        e.preventDefault();
                        var message = $('#chat-input').val();
                        $.ajax({
                            url: '/chatbot',
                            data: {message: message},
                            success: function(response) {
                                $('<p>').text(response.message).appendTo('#chat-container');
                                $('#chat-input').val('');
                            },
                            error: function(error) {
                                console.log(error);
                            }
                        });
                    });
                });
            </script>
        </html>
    '''

@app.route('/chatbot', methods=['GET'])
def chatbot():
    message = request.args.get('message')
    response = get_response(message)
    return jsonify({'message': response})

if __name__ == '__main__':
    app.run(debug=True)
