# https://github.com/DonatasNoreika/Python-pamokos/wiki/Flask:-nuotraukos-prid%C4%97jimas,-admin-puslapis,-puslapiavimas

# Flask: nuotraukos pridėjimas, admin puslapis, puslapiavimas
# DonatasNoreika edited this page on Mar 23, 2021 · 9 revisions

# Kaip pridėti nuotrauką (paskyros redagavimas)
# Papildome sqlalchemy klasę:

# class Vartotojas(db.Model, UserMixin):
#     __tablename__ = "vartotojas"
#     id = db.Column(db.Integer, primary_key=True)
#     vardas = db.Column("Vardas", db.String(20), unique=True, nullable=False)
#     el_pastas = db.Column("El. pašto adresas", db.String(120), unique=True, nullable=False)
#     nuotrauka = db.Column(db.String(20), nullable=False, default='default.jpg')
#     slaptazodis = db.Column("Slaptažodis", db.String(60), unique=True, nullable=False)

# Pridedame paskyros redagavimo formą:

# from flask_wtf.file import FileField, FileAllowed

# class PaskyrosAtnaujinimoForma(FlaskForm):
#     vardas = StringField('Vardas', [DataRequired()])
#     el_pastas = StringField('El. paštas', [DataRequired()])
#     nuotrauka = FileField('Atnaujinti profilio nuotrauką', validators=[FileAllowed(['jpg', 'png'])])
#     submit = SubmitField('Atnaujinti')

#     def tikrinti_varda(self, vardas):
#         if vardas.data != app.current_user.vardas:
#             vartotojas = app.Vartotojas.query.filter_by(vardas=vardas.data).first()
#             if vartotojas:
#                 raise ValidationError('Šis vardas panaudotas. Pasirinkite kitą.')

#     def tikrinti_pasta(self, el_pastas):
#         if el_pastas.data != app.current_user.el_pastas:
#             vartotojas = app.Vartotojas.query.filter_by(el_pastas=el_pastas.data).first()
#             if vartotojas:
#                 raise ValidationError('Šis el. pašto adresas panaudotas. Pasirinkite kitą.')
            
# Panašiai, kaip ir registracijos formoje, tik vardo ir el. pašto tikrinimo metodai papildomai patikrina, 
# ar įvestas vardas ar el. paštas nesutampa su prisijungtu vartotoju ir tik tada atlieka patikrinimus. 
# Taip pat pridėtas FileField tipo nuotrauka laukas su FileAllowed validatoriumi. Juos reikia suimportuoti iš flask_wtf.file.

# Pakeičiame paskyros atvaizdavimo puslapį:

# {% extends "base.html" %}
# {% block content %}
# <div class="content-section">
#     <form method="POST" action="" enctype="multipart/form-data">
#         {{ form.hidden_tag() }}
#         <fieldset class="form-group">
#             <legend class="border-bottom mb-4">Paskyros informacija</legend>
#             <img class="rounded-circle account-img" src="{{ nuotrauka }}">
#             <div class="form-group">
#                 {{ form.vardas.label(class="form-control-label") }}

#                 {% if form.vardas.errors %}
#                 {{ form.vardas(class="form-control form-control-lg is-invalid") }}
#                 <div class="invalid-feedback">
#                     {% for error in form.vardas.errors %}
#                     <span>{{ error }}</span>
#                     {% endfor %}
#                 </div>
#                 {% else %}
#                 {{ form.vardas(class="form-control form-control-lg") }}
#                 {% endif %}
#             </div>
#             <div class="form-group">
#                 {{ form.el_pastas.label(class="form-control-label") }}
#                 {% if form.el_pastas.errors %}
#                 {{ form.el_pastas(class="form-control form-control-lg is-invalid") }}
#                 <div class="invalid-feedback">
#                     {% for error in form.el_pastas.errors %}
#                     <span>{{ error }}</span>
#                     {% endfor %}
#                 </div>
#                 {% else %}
#                 {{ form.el_pastas(class="form-control form-control-lg") }}
#                 {% endif %}
#             </div>
#             <div class="form-group">
#                 {{ form.nuotrauka.label() }}
#                 {{ form.nuotrauka(class="form-control-file") }}
#                 {% if form.nuotrauka.errors %}
#                     {% for error in form.nuotrauka.errors %}
#                         <span class="text-danger">{{ error }}</span></br>
#                     {% endfor %}
#                 {% endif %}
#             </div>
#         </fieldset>
#         <div class="form-group">
#             {{ form.submit(class="btn btn-outline-info") }}
#         </div>
#     </form>
# </div>
# {% endblock content %}

# Panašus puslapis, kaip ir registracijos formoje, bet paliktas tik vardo ir el. pašto redagavimas.
# Taip pat įdėtas nuotraukos redagavimas ir atvaizdavimas (žr. img). Atkreipkite dėmesį, kad į 
# formos žymą įdėtas parametras enctype="multipart/form-data", kad galėtume pridėti ir failą.

# Pakeičiame paskyros Flask funkciją:

# @app.route("/paskyra", methods=['GET', 'POST'])
# @login_required
# def paskyra():
#     form = forms.PaskyrosAtnaujinimoForma()
#     if form.validate_on_submit():
#         if form.nuotrauka.data:
#             nuotrauka = save_picture(form.nuotrauka.data)
#             current_user.nuotrauka = nuotrauka
#         current_user.vardas = form.vardas.data
#         current_user.el_pastas = form.el_pastas.data
#         db.session.commit()
#         flash('Tavo paskyra atnaujinta!', 'success')
#         return redirect(url_for('paskyra'))
#     elif request.method == 'GET':
#         form.vardas.data = current_user.vardas
#         form.el_pastas.data = current_user.el_pastas
#     nuotrauka = url_for('static', filename='profilio_nuotraukos/' + current_user.nuotrauka)
#     return render_template('paskyra.html', title='Account', form=form, nuotrauka=nuotrauka)

# Paaiškinimai:

# Atkeipkite dėmesį, kad atnaujinant duomenis, vartotojas ne ieškomas duomenų bazėje, o tiesiog pakeičiami prisijungto vartotojo 
# (current_user) duomenys ir padaromas db.session.commit(). To užtenka norint atnaujinti vartotojo duomenis.
# elif skiltyje formai prisikiriamas vartotojo vardas ir el. paštas, kad redaguojamoje formoje šie laukai jau
# būtų užpildyti, beliktų juos pakeisti redaguojant.
# Jei formoje prisegama nuotrauka, ji pasiimama (jos pavadinimas), priskiriama prisijungusiam vartotojui. 
# Tuomet prieš return nuotrauka pasiimama iš static katalogo ir paduodama atgal į formą.
# Pridėdame nuotraukos išsaugojimo funkciją:

# import secrets
# from PIL import Image

# def save_picture(form_picture):
#     random_hex = secrets.token_hex(8)
#     _, f_ext = os.path.splitext(form_picture.filename)
#     picture_fn = random_hex + f_ext
#     picture_path = os.path.join(app.root_path, 'static/profilio_nuotraukos', picture_fn)

#     output_size = (125, 125)
#     i = Image.open(form_picture)
#     i.thumbnail(output_size)
#     i.save(picture_path)

#     return picture_fn

# Paaiškinimai:

# Ši funkcija pasiima nuotrauką (iš formos), išsaugo ją 'static/profilio_nuotraukos' kataloge ir gražina nuotraukos pavadinimą, 
# kuris vėliau išsaugomas vartotojo DB lentelėje.
# random_hex sugeneruojamas atsitiktinis 8 simboliu stringas.
# Kitoje eilutėje pasiimamas formoje išsaugoto failo plėtinys.
# Vėliau prie sugeneruoto stringo prijungiamas plėtinys.
# Nustatomas picture_path - pilnas kelias iki paveikslėlio
# Kitose keturiose eilutėse nustatomas miniatiūros dydis, per Pillow atidaroma nuotrauka, pamažinama nustatytu dydžiu ir 
# išsaugoma prieš tai sugeneruotu pavadinimu.
# Funkcija gražina tą sugeneruotą pavadinimą.
# Kaip į svetainę įdėti automatinį admin puslapį

# from flask_admin import Admin
# from flask_admin.contrib.sqla import ModelView

# class ManoModelView(ModelView):
#     def is_accessible(self):
#         return current_user.is_authenticated and current_user.el_pastas == "el@pastas.lt"

# admin = Admin(app)
# admin.add_view(ModelView(Irasas, db.session))
# admin.add_view(ManoModelView(Vartotojas, db.session))
# Paaiškinimai:

# Importuojame Admin ir ModelView objektus iš flask_admin modulio
# Inicijuojame Admin objektą ir priskiriame app.
# Administratoriui priskiriame norimus administruoti sqlalchemy objektus. Pirmu atveju daromas paprastas priskyrimas, antru – priskirta paveldėtas ManoModelView objektas ir jame perrašomas is_accesisible metodas taip, kad puslapis būtų rodomas tik tuo atveju, kai vartotojas prisijungęs ir jo el. pašto adresas yra el@pastas.lt (jį galima pakeisti).
# Įrašų puslapiavimas svetainėje
# Pakoreguojame įrašų atvaizdavimą Flask punkcijoje:

# @app.route("/irasai")
# @login_required

# def records():
#     db.create_all()
#     page = request.args.get('page', 1, type=int)
#     visi_irasai = Irasas.query.filter_by(vartotojas_id=current_user.id).order_by(Irasas.data.desc()).paginate(page=page, per_page=5)
#     return render_template("irasai.html", visi_irasai=visi_irasai, datetime=datetime)

# Paaiškinimai:

# page = pasiima http iš užklausos page objektą, defaultu nustato 1 ir nurodo integer tipą (type=int)
# visi įrašai užklausoje kviečiame .paginate() funkciją ir jai paduodame prieš tai gautą page objektą bei kiek įrašų norėsime matyti viename puslapyje.
# Įrašai taip pat rūšiuojami pagal datą atbulai, kad naujausi būtų matomi pirmajame puslapyje.
# Taip pat filtruojami, kad būtų rodomi tik priklausantys prisijungusiam vartotojui.
# Pakeičiame susijusį html puslapį:

# {% extends "base.html" %}

# {% block content %}

# {% if visi_irasai %}
# {% for irasas in visi_irasai.items %}
# <hr>
# {% if irasas.pajamos %}
# <p>Pajamos: {{irasas.suma}}</p>
# <p>Data: {{ datetime.strftime(irasas.data, "%Y-%m-%d %H:%M:%S")}}</p>
# {% else %}
# <p>Išlaidos: {{irasas.suma}}</p>
# <p>Data: {{irasas.data}}</p>
# {% endif %}
# <a href="{{ url_for('delete', id=irasas['id']) }}">Ištrinti</a>
# <a href="{{ url_for('update', id=irasas['id']) }}">Redaguoti</a>
# {% endfor %}
# <hr>
# {% for page_num in visi_irasai.iter_pages(left_edge=1, right_edge=1, left_current=1, right_current=2) %}
#   {% if page_num %}
#     {% if visi_irasai.page == page_num %}
#       <a class="btn btn-info mb-4" href="{{ url_for('records', page=page_num) }}">{{ page_num }}</a>
#     {% else %}
#       <a class="btn btn-outline-info mb-4" href="{{ url_for('records', page=page_num) }}">{{ page_num }}</a>
#     {% endif %}
#   {% else %}
#     ...
#   {% endif %}
# {% endfor %}
# {% endif %}

# <p><a href="{{ url_for('new_record')}}">Naujas įrašas</a></p>

# {% endblock %}

# Paaiškinimai:

# Pirmame for cikle pakeičiame visi_irasai į visi_irasai.items. Taip išvengsime iteravimo klaidos.
# Po visų įrašų for ciklo, įdedame papildomą for ciklą per įrašus. Iškviečiame funkciją .iter_pages() ir jai nurodome, 
# kiek puslapių mygtukų norėsime kairėje, dešinėje, prieš ir už aktyvaus puslapio.
# Pirmas {% if page_num %} prafiltruoja tik aktyvius puslapius, nes sąraše visi_irasai.iter_pages() lieka ir None objektų.
# Antras {% if visi_irasai.page == page_num %} atfiltruoja aktyvaus puslapio rodinį: jam pritaikytas kitoks stilius (spalva), 
# nei neaktyviems puslapiams, kurių rodinys atvaizduojamas {% else %} skiltyje.