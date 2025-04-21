# Mapa weba

* landing unlogged
    - registracija
        - ime, prezime, email, pass
    - login
* landing logged user
    - vidi smjerove
    - upiši se u smjer
        * podaci za upis
            - datum  rođenja (date picker)
            - mjesto rođenja (line input)
            - završena škola (line input)
            - mobla za upis (file upload)
            - odabir smjera (muliple picker?)
            - dokument o završetku (file upload)
            - prosjek ocjena (line input + validation)
            - ocjena na maturi (line input ili choice)
        * popup obavjest da je pun
        * ako se upiše više ne može upisati, ali može gledati
* landing logged admin
    - vidi prijave
    - vidi studente
    - upiši studenta
        + navedi razlog odobrenja
        * zabilježiti tko je odobrio
    - kreiraj administratore
    - izbriši administratore

# Database

* korisnik
    * id
    * ime
    * prezime
    * email
    * password?!
    * status (student, administrator)
* predmet
    * id
    * naziv
    * opis
    * nositelj
    * ects
* smjer
    * id
    * naziv
    * kvota
    * slobodna mjesta
* predmeti po smjeru (m:n)
    * id
    * id smjera
    * id predmeta
* prijave
    * id korisnika
    * id smjera
* upis
    * id upisanog usera
    * vrijeme odobrenja
    * objašnjenje odobrenja
    * id upisnika


# Routes

/
    landing
/smjerovi
    +popis smjerova, kvote i slobodnih mjesta
/smjerovi/<smjer>
    +informacija o smjeru s listom predmeta i ETCS bodova
/smjerovi/<smjer>/<predmet>
    +opis predmeta s nazivom, ects bodovima, imenom nositelja i opisom
/smjerovi/<smjer>/prijava
    +izravna prijava na dani smjer - formular sa smjerom ispunjenim
/prijava
    +formular za prijavu
/prijave
    popis prijava s korisnicima i prijavljenim smjerom
/prijave/<broj prijave>
    stranica za odobrenje i negiranje prijave
    mjesto za unos razloga zašto
/korisnici
    +stranica za pregledavanje dodavanje i brisanje korisnika (administratora)
/korisnici/novi
    +stranica za unos novog korisnika

# TODO
- pregled prijava i odobravanje
- dodavanje i brisanje korisnika i administratora