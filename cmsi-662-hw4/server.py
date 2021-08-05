from flask import Flask, render_template, request
from datetime import date

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/greet', methods=["POST"])
def greet():
    try:
        date_format = "%m-%d-%Y"
        full_name_max_length = 50
        
        full_name_object = request.form.get("name")
        birthdate_object = request.form.get("birthdate")

        # Check for empty full_name_object
        if full_name_object == '':
            raise EOFError

        # Check for the max length of a name
        if len(full_name_object) > full_name_max_length:
            raise EOFError

        # Convert birthdate from string to date
        birthdate = date.fromisoformat(birthdate_object)
        today = date.today()
        # I attempted to use timedelta here, but it seemed to make the code more complex
        age_days = (today - birthdate).days
        age_years = round(age_days / 365, 2)

        # Format dates to be more easily readable by the client
        birthdate_formatted = birthdate.strftime(date_format)
        today_formatted = today.strftime(date_format)

        # Check for future dated birthdate
        assert age_years > 0

        ##
        # Rather than writing HTML in the return function, when a programmer renders html through a template, XSS is prevented automatically.
        # The routes in the app are sending data back to the client through templates instead of directly from HTML.
        # #
        return render_template('greet.html',
                                full_name_object=full_name_object,
                                birthdate_object=birthdate_object,
                                birthdate=birthdate,
                                birthdate_formatted=birthdate_formatted,
                                today=today,
                                today_formatted=today_formatted,
                                age_days=age_days,
                                age_years=age_years,)
    except EOFError:
        return render_template("/errors/name-error.html")
    except ValueError:
        return render_template("/errors/date-error.html")
    except AssertionError:
        return render_template("/errors/age-error.html",
                                age_years=age_years,)

if __name__ == '__main__':
    app.run(debug=True)