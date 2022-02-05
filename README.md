Tietokantasovellus - Fuksisuunnistus
====================================

### Mikä on fuksisuunnistus?
Fuksisuunnistus on syksyisin järjestettävä ensimmäisen vuoden opiskelijoille suunnattu tapahtuma, jossa kierretään pienissä ryhmissä Kumpulan lähiympäristössä lähinnä tuutorien pitämiä rasteja. Rasteilla suoritetaan lyhyt tehtävä, jonka rastinvetäjät arvioivat. Tehtävän lisäksi pisteytetään suorittavan ryhmän mahdolliset asut, ryhmähenki ja muut huomionarvoiset asiat. Eniten pisteitä keränneet ryhmät palkitaan Fuksiaisissa, jotka toimivat suunnistuksen jatkotapahtumana. 

---
Sovellus
--------
Sovellus toimii välineenä rastinvetäjille TKO-älyn fuksisuunnistussuoritusten arvioinnissa. Aiemmin arviointiin on käytetty kynää ja paperia tai Google Sheetsia. Sovelluksen avulla pyritään helpottamaan erityisesti arviointien kirjaamista rasteilla sekä loppupisteiden laskentaa.

Sovellus on käytettävissä [Herokussa](https://fuksisuunnistus.herokuapp.com/).

### Kuvaus
Sovellukseen kirjaudutaan sisään joko ylläpitäjänä tai käyttäjänä. Käyttäjän roolissa toimivat rastinvetäjät, ylläpitäjätunnusta käyttävät tuutorivastaavat. Rasteja kiertävät ryhmät kirjataan tuutorivastaavien toimesta sovellukseen lähdössä, mutta suunnistajat eivät toimi sovelluksen käyttäjinä. Tuutorivastaavilla on ennalta suunniteltu reitti ja he kertovat ryhmän ensimmäisen rastin sijainnin ryhmälle. Rastinvetäjät kertovat ryhmälle seuraavan sijainnin. Rastinvetäjät lisäävät suorituksen valiten listasta ryhmän, täyttäen pisteytyskentät ja kirjoittamalla lyhyen sanallisen kuvauksen (vapaaehtoinen).

#### Ylläpitäjä (tuutorivastaavat):
* Yksi tili, vaikka ylläpitäjiä olisi useampia
* Hallinnoi käyttäjiä (rasteja)
  * Lisää käyttäjät
  * Pystyy poistamaan käyttäjän
  * Pystyy muokkaamaan käyttäjien tietoja
* Näkee kaikkien käyttäjien tiedot
  * listattuna kohdassa [Käyttäjä](https://github.com/kvjanhun/tsoha-fuksisuunnistus#k%C3%A4ytt%C3%A4j%C3%A4-rastinvet%C3%A4j%C3%A4t)
* Lisää suunnistuksen aluksi suunnistavat ryhmät sovellukseen
  * Ryhmän nimi
  * Ryhmän koko
* Näkee yhteenvedon ryhmien suorituksista
  * Rastikohtaiset suoritukset pisteineen
  * Yhteispisteet (kaikilta rasteilta)

#### Käyttäjä (rastinvetäjät):
* Näkee omat tietonsa
  * Rastin nimi
  * Rastin vetäjien nimet
  * Puhelinnumero
  * Rastin sijainti
  * Montako suoritusta kirjattu
  * Seuraavan rastin sijainti, vetäjät ja puhelinnumero
* Pystyy muokkaamaan rastinsa sijaintia
* Pystyy lisäämään suunnistusryhmien suorituksia rastilleen
  * Pystyy muokkaamaan suorituksia
* Ei näe muiden rastien tietoja eikä heidän merkkaamiaan suorituksia

### Nykytilanne
Sovelluksen toiminnallisuus on vielä toteuttamatta. Sovelluksen rakenne ja tietokanta ovat kuitenkin suunniteltu. Sovelluksen raakile on julkaistu Herokuun.
