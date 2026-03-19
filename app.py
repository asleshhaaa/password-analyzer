from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    pattern_info = ""
    suggestions = []

    if request.method == "POST":
        password = request.form["password"]

        # ✅ Empty check
        if password.strip() == "":
            result = "Please enter a password ⚠️"
            return render_template("index.html", result=result, pattern="", suggestions=[])

        # ✅ Conditions
        length = len(password) >= 8
        upper = any(char.isupper() for char in password)
        lower = any(char.islower() for char in password)
        digit = any(char.isdigit() for char in password)
        special = any(not char.isalnum() for char in password)

        # ✅ Improved scoring system
        score = 0

        if len(password) >= 8:
            score += 2
        if len(password) >= 12:
            score += 1
        if upper:
            score += 1
        if lower:
            score += 1
        if digit:
            score += 1
        if special:
            score += 2

        # ✅ Strength result
        if score <= 3:
            result = "Weak Password ❌"
        elif score <= 6:
            result = "Medium Password ⚠️"
        else:
            result = "Strong Password ✅"

        # ✅ Pattern detection (improved)
        common_passwords = ["password", "123456", "qwerty", "admin"]

        if password.lower() in common_passwords:
            pattern_info = "Very Common Password (~80%)"
        elif password.isalpha():
            pattern_info = "Only letters pattern (~50%)"
        elif password.isdigit():
            pattern_info = "Only numbers pattern (~70%)"
        elif any(char.isdigit() for char in password) and any(char.isalpha() for char in password):
            pattern_info = "Word + numbers pattern (~60%)"
        else:
            pattern_info = "Strong/rare pattern (~10-20%)"

        # ✅ Suggestions
        if not length:
            suggestions.append("Use at least 8 characters")
        if not upper:
            suggestions.append("Add uppercase letters (A-Z)")
        if not lower:
            suggestions.append("Add lowercase letters (a-z)")
        if not digit:
            suggestions.append("Include numbers (0-9)")
        if not special:
            suggestions.append("Add special characters (!@#$)")

    return render_template("index.html", result=result, pattern=pattern_info, suggestions=suggestions)


if __name__ == "__main__":
    app.run(debug=True)