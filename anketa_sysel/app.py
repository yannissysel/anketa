from flask import Flask, render_template, redirect, session
from flask_wtf import FlaskForm
from wtforms import RadioField
import sqlite3

app = Flask(__name__)
app.debug = True
app.secret_key = "dadada bababa cacaca vavava"

class AnketaForm(FlaskForm):
    hlas = RadioField(choices=[("mercedes", "Mercedes"), ("bmw", "BMW"), ("audi", "Audi")])

@app.route('/', methods=["GET", "POST"])
def hlasovani():
    if 'uz_hlasoval' in session:
        return redirect('/odhlasovano')
    form = AnketaForm()
    hlas_uzivatele = form.hlas.data
    if form.validate_on_submit():
        try:
            con = sqlite3.connect("./anketa.db")
            cur = con.cursor()
            cur.execute("INSERT INTO anketa(odpoved) VALUES(?)", (hlas_uzivatele,))
            con.commit()
            con.close()
            session['uz_hlasoval'] = True
            return redirect('/odhlasovano')
        except:
            return redirect('/')
    return render_template('index.html', form=form)

@app.route('/odhlasovano')
def odhlasovano():
    con = sqlite3.connect("./anketa.db")
    cur = con.cursor()
    odpovedi = cur.execute("SELECT COUNT(odpoved) FROM anketa WHERE odpoved='mercedes'")
    vysledky_mercedes = odpovedi.fetchone()
    odpovedi = cur.execute("SELECT COUNT(odpoved) FROM anketa WHERE odpoved='bmw'")
    vysledky_bmw = odpovedi.fetchone()
    odpovedi = cur.execute("SELECT COUNT(odpoved) FROM anketa WHERE odpoved='audi'")
    vysledky_audi = odpovedi.fetchone()
    con.close()
    return render_template('odhlasovano.html', vysledky_mercedes=vysledky_mercedes[0], vysledky_bmw=vysledky_bmw[0], vysledky_audi=vysledky_audi[0])

if __name__ == '__main__':
    app.run()
