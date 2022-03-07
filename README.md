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
Sovellukseen kirjaudutaan sisään luodulla tunnuksella. Käyttäjän roolissa toimivat rastinvetäjät, ylläpitäjätunnusta käyttävät tuutorivastaavat. Ylläpitäjän rooli asetetaan tietokantaan suoraan, sillä tarve on käytännössä vain yhdelle ylläpitäjätunnukselle. Rasteja kiertävät ryhmät kirjataan tuutorivastaavien toimesta sovellukseen lähdössä, mutta suunnistajat eivät toimi sovelluksen käyttäjinä. Tuutorivastaavilla on ennalta suunniteltu reitti ja he kertovat ryhmän ensimmäisen rastin sijainnin ryhmälle. Rastinvetäjät kertovat ryhmälle seuraavan sijainnin. Rastinvetäjät lisäävät suorituksen valiten listasta ryhmän, täyttäen pisteytyskentät ja kirjoittamalla lyhyen sanallisen kuvauksen (vapaaehtoinen).

#### Ylläpitäjä (tuutorivastaavat):
* Yksi tili, vaikka ylläpitäjiä olisi useampia
* Hallinnoi käyttäjiä
  * Pystyy poistamaan käyttäjän
  * Pystyy muokkaamaan käyttäjien tietoja
* Näkee kaikkien käyttäjien tiedot
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
* Pystyy muokkaamaan rastinsa tietoja
* Pystyy lisäämään suunnistusryhmien suorituksia rastilleen
  * Pystyy muokkaamaan suorituksia
* Ei näe muiden rastien tietoja eikä heidän merkkaamiaan suorituksia, vain järjestyksessä seuraavan rastin sijainnin ja vetäjät

### Nykytilanne
Sovellus on vielä osittain keskeneräinen, mutta keskeisimmät toiminnallisuudet ovat toteutettu. Sovellus on käytettävissä [Herokussa](https://fuksisuunnistus.herokuapp.com/).

#### Toteutettu toiminnallisuus:
* Käyttäjätunnusten luominen ja kirjautuminen
* Rastin tietojen tallentaminen ja muokkaaminen.
* Ylläpitäjän Kaikki rastit -sivu listaa kaikki tietokantaan tallennetut rastit.
* Yksittäisten rastien tarkastelu ja muokkaus Ylläpitäjä-sivulla.
* Ylläpitäjä voi lisätä ja poistaa joukkueita.
* Käyttäjä voi arvostella joukkueita.
* Ylläpitäjä näkee joukkueiden sijoitukset.

#### Muutokset edellisestä välipalautuksesta:
* Herokun tietokanta on resetoitu, joten vanhat käyttäjätunnukset eivät toimi.
* Uudelle käyttäjälle luodaan rasti ja tiedot ensimmäisen kirjautumisen yhteydessä.
* Ylläpitäjä voi muokata rastien tietoja.
* Virheilmoitukset esitetään samalla sivulla kuin mistä virhe on peräisin. Lomakkeiden tiedot tallennetaan ja näytetään lomakkeessa virheen jälkeen.
* Ylläpitäjä voi lisätä ja poistaa joukkueita.
* SQL-skeemaa päivitetty riippuvuuksien huomioimiseksi.
* Rekisteröitymistä paranneltu, mm. tarkastetaan ettei käyttäjätunnus ole jo käytössä.
* Käyttäjät voivat arvostella joukkueita.
* Ylläpitäjä näkee joukkueiden sijoitukset.

#### Ominaisuudet vielä työn alla:
* Joukkueiden arvostelemista pitäisi parantaa
  * Käyttöliittymä on kömpelö, sillä "Näytä"-painike jää helposti painamatta ja tällöin joukkue ei ole vielä valittu eikä arvostelu onnistu.
* Joukkueille tulisi toteuttaa joukkuekohtaiset sivut, josta näkee valitun joukkueen arvostelut rasteittain.
* Rasteille muutettavissa oleva järjestysnumero tietokantaan. Tämä näkyviin rastin numerona nykyisen id:n sijaan. Tämä on osittain toteutettu, mutta ei vielä käytössä. Nykyisellään rastien järjestys täytyy tapahtua sovelluksen ulkopuolella eikä sovelluksessa ole ominaisuutta näyttää seuraavaa rastia rastinvetäjille.

### Tulevaisuus
Sovellus ei ole vielä valmis. Sovelluksen kehittäminen jatkuu harrastusprojektina ja se on tavoitteena saada varteenotettavaksi vaihtoehdoksi taulukoinnille fuksisuunnistuksiin.