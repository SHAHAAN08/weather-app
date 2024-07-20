from flask import Flask, render_template_string, request, jsonify,url_for
import requests
from datetime import datetime
import webview

app = Flask(__name__)


window = webview.create_window("Weather app", app, width=420, height=650)


HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&family=Roboto:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <title>Weather App</title>
    <style>
        *{
            margin: 0;
            padding: 0;
            border: 0;
            outline: none;
            box-sizing: border-box;
        }

        body{
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            background: white;
        }

        .container{
            position: relative;
            width: 400px;
            height: 105px;
            background: #fff;
            padding: 28px 32px;
            overflow: hidden;
            border-radius: 18px;
            font-family: 'Roboto', sans-serif;
            transition: 0.6s ease-out;
        }

.search-box {
    width: 100%;
    height: min-content;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border: 2px solid black; /* Black border */
    border-radius: 25px; /* Curved border radius */
    padding: 10px; /* Padding */
}

.search-box input {
    color: #06283D;
    width: 80%;
    font-size: 24px;
    font-weight: 500;
    text-transform: uppercase;
    padding-left: 32px;
    border: none; /* Remove default input border */
    outline: none; /* Remove input outline */
}

.search-box input::placeholder {
    font-size: 20px;
    font-weight: 500;
    color: #06283D;
    text-transform: capitalize;
}

.search-box button {
    cursor: pointer;
    width: 50px;
    height: 50px;
    color: #06283D;
    background: #dff6ff;
    border-radius: 50%;
    font-size: 22px;
    transition: 0.4s ease;
    border: none; /* Remove default button border */
    outline: none; /* Remove button outline */
}

.search-box button:hover {
    color: #fff;
    background: #06283D;
}

.search-box i {
    position: absolute;
    color: #06283D;
    font-size: 28px;
}


        .weather-box{
            text-align: center;
        }

        .weather-box img{
            width: 60%;
            margin-top: 30px;
        }

        .weather-box .temperature{
            position: relative;
            color: #06283D;
            font-size: 4rem;
            font-weight: 800;
            margin-top: 30px;
            margin-left: -16px;
        }

        .weather-box .temperature span{
            position: absolute;
            margin-left: 4px;
            font-size: 1.5rem;
        }

        .weather-box .description{
            color: #06283D;
            font-size: 22px;
            font-weight: 500;
            text-transform: capitalize;
        }

        .weather-details{
            width: 100%;
            display: flex;
            justify-content: space-between;
            margin-top: 30px;
        }

        .weather-details .humidity, .weather-details .wind{
            display: flex;
            align-items: center;
            width: 50%;
            height: 100px;
        }

        .weather-details .humidity{
            padding-left: 20px;
            justify-content: flex-start;
        }

        .weather-details .wind{
            padding-right: 20px;
            justify-content: flex-end;
        }

        .weather-details i{
            color: #06283D;
            font-size: 26px;
            margin-right: 10px;
            margin-top: 6px;
        }

        .weather-details span{
            color: #06283D;
            font-size: 22px;
            font-weight: 500;
        }

        .weather-details p{
            color: #06283D;
            font-size: 14px;
            font-weight: 500;
        }

        .not-found{
            width: 100%;
            text-align: center;
            margin-top: 50px;
            scale: 0;
            opacity: 0;
            display: none;
        }

        .not-found img{
            width: 70%;
        }

        .not-found p{
            color: #06283D;
            font-size: 22px;
            font-weight: 500;
            margin-top: 12px;
        }

        .weather-box, .weather-details{
            scale: 0;
            opacity: 0;
        }

        .fadeIn{
            animation: 0.5s fadeIn forwards;
            animation-delay: 0.5s;
        }

        @keyframes fadeIn{
            to {
                scale: 1;
                opacity: 1;
            }
        }
    </style>
</head>
<body>

    <div class="container">
        <div class="search-box">
            <i class="fa-solid fa-location-dot"></i>
            <input type="text" placeholder="Enter your location" id="cityInput">
            <button class="fa-solid fa-magnifying-glass" id="searchBtn"></button>
        </div>

        <div class="not-found">
            <img src="{{ url_for('static', filename='images/404.png') }}">
            <p>Oops! Invalid location :/</p>
        </div>

        <div class="weather-box">
            <img src="" id="weatherIcon">
            <p class="temperature" id="temperature"></p>
            <p class="description" id="description"></p>
        </div>

        <div class="weather-details">
            <div class="humidity">
                <i class="fa-solid fa-water"></i>
                <div class="text">
                    <span id="humidity"></span>
                    <p>Humidity</p>
                </div>
            </div>
            <div class="wind">
                <i class="fa-solid fa-wind"></i>
                <div class="text">
                    <span id="wind"></span>
                    <p>Wind Speed</p>
                </div>
            </div>
        </div>

    </div>

    <script src="https://kit.fontawesome.com/7c8801c017.js" crossorigin="anonymous"></script>
    <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
    <script>
        $(document).ready(function() {
            $('#searchBtn').click(function() {
                var city = $('#cityInput').val();
                if (city === '') return;

                $.ajax({
                    url: '/weather',
                    type: 'POST',
                    data: { city: city },
                    success: function(response) {
                        if (response.error) {
                            $('.container').css('height', '400px');
                            $('.weather-box').hide();
                            $('.weather-details').hide();
                            $('.not-found').show().addClass('fadeIn');
                        } else {
                            $('.not-found').hide().removeClass('fadeIn');
                            $('#weatherIcon').attr('src', response.icon);
                            $('#temperature').html(response.temperature);
                            $('#description').html(response.description);
                            $('#humidity').html(response.humidity);
                            $('#wind').html(response.wind);

                            $('.weather-box').show().addClass('fadeIn');
                            $('.weather-details').show().addClass('fadeIn');
                            $('.container').css('height', '590px');
                        }
                    },
                    error: function(error) {
                        alert('Error fetching weather data.');
                    }
                });
            });
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/weather', methods=['POST'])
def get_weather():
    api_key = '312bf436357c548bedcd96af660aef7b'  # Replace with your OpenWeatherMap API key
    city = request.form['city']

    current_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(current_url)
    data = response.json()

    if data['cod'] == '404':
        return jsonify({'error': 'City not found!'})

    temperature = f"{int(data['main']['temp'])}°C"
    description = data['weather'][0]['description']
    humidity = f"{data['main']['humidity']}%"
    wind = f"{int(data['wind']['speed'])}Km/h"
    
    icon_map = {
        'Clear': 'images/clear.png',
        'Rain': 'images/rain.png',
        'Snow': 'images/snow.png',
        'Clouds': 'images/cloud.png',
        'Haze': 'images/mist.png'
    }
    icon = icon_map.get(data['weather'][0]['main'], '')

    return jsonify({
        'temperature': temperature,
        'description': description,
        'humidity': humidity,
        'wind': wind,
        'icon': url_for('static', filename=icon)
    })

if __name__ == '__main__':
    webview.start()
