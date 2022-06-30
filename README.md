# YpoxreotikiErgasia22_e16001_Agoropoulos_Stelios
Εργασία εξαμήνου για το μάθημα "Πληροφοριακά Συστήματα" Εαρινό 2022 - Αγορόπουλος Στέλιος e16001.

Για οποιαδήποτε πληροφορία σχετικά με την εργασία, μπορείτε να επικοινωνήσετε μαζί μου στο sagoropoulos@gmail.com

# Οδηγίες εγκατάστασης & εκτέλεσης

Για να καταστεί εφικτή η εκτέλεση του παραπάνω συστήματος, απαιτείται η εγκατάσταση του Docker και του Docker Compose.

## Docker Desktop & Docker Compose

Υπάρχει διαθέσιμη εφαρμογή "Docker Desktop" για Mac,Windows και Linux,  η οποία περιλαμβάνει το Docker και το Docker Compose.

Το μόνο που χρειάζεται να κάνει ο χρήστης είναι να κατεβάσει το εκτελέσιμο αρχείο και να προχωρήσει στην εγκατάσταση.

**Download Link**: https://www.docker.com/products/docker-desktop/

Αναλυτικές οδηγίες εγκατάστασης και System Requirements ανα πλατφόρμα, μπορούν να βρεθούν εδώ : https://docs.docker.com/desktop/

## Εγκατάσταση Docker για Linux

Για την εγκατάσταση του Docker σε Linux είναι απαραίτητη η εκτέλεση των παρακάτω εντολών στο Terminal.

```
 $ sudo apt-get update
 
 $ sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
 
 $ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key
add -

 $ sudo add-apt-repository -y "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

 $ sudo apt-get update

 $ sudo apt install docker-ce
```

## Εγκατάσταση Docker Compose για Linux

Για την εγκατάσταση του Docker Compose plugin σε Linux είναι απαραίτητη η εκτέλεση των παρακάτω εντολών στο Terminal.
```
 $ sudo apt-get update
 $ sudo apt-get install docker-compose-plugin
```

## Containerization & Εκτέλεση Εφαρμογής

Αρχικά, θα πρέπει να γίνει clone το συγκεκριμένο Repository ή Download as ZIP και να βάλετε τα περιεχομενα του σε ένα directory στο σύστημά σας.

Στη συνέχεια, έχοντας εγκαταστήσει το Docker και το Docker Compose, για να δημιουργήσουμε μια Containerized εκδοχή της εφαρμογή μας που θα αλληλεπιδρά με την MongoDB θα πρέπει να εκτελεστεί η παρακάτω εντολή : 

```
 $ (sudo) docker-compose up -d
```

Για τον τερματισμό της εφαρμογής θα πρέπει να εκτελεστεί η παρακάτω εντολή : 
```
 $ (sudo) docker-compose up -d
```

# Λειτουργίες συστήματος

Παρακάτω, μπορείτε να διαβάσετε αναλυτικά όλες τις λειτουργίες του συστήματος. Δίνονται αναλυτικές πληροφορίες για κάθε endpoint, καθώς και παραδείγματα εκτελέσεων.

### Δοκιμές λειτουργιών
Έχει γίνει publish ένα Workspace στο Postman, το οποίο μπορείτε να χρησιμοποιήσετε για να πραγματοποιήσετε όλες τις απαραίτητες δοκιμές.
**Είναι απαραίτητο να έχετε λογαριασμό στο Postman**.

Workspace URL : https://www.postman.com/gold-crescent-810855/workspace/infosys-python-e16001-agoropoulos-stelios/overview

## Authentication Scheme & Session Management

Στο συγκεκριμένo σύστημα, υποστηρίζεται HTTP Basic Authentication. 

Για την χρήση των υπηρεσιών του συστήματος από έναν χρήστης είναι απαραίτητο αρχικά να έχει λογαριασμό στο σύστημα και να έχει πραγματοποιήσει είσοδο σε αυτό. Μόλις πραγματοποιήσει επιτυχή είσοδο θα δημιουργηθεί ένα session και το σύστημα θα του επιστρέψει το παρακάτω response : 

```json
{
    "Authorization Key": "aa1ea2e6-f86c-11ec-81e3-0242ac180003",
    "username": "admin@infosys.gr",
    "message": "Login successful!"
}
```

Στη συνέχεια, **για τα endpoints στα οποία απαιτείται authorization header**, ο χρήστης θα πρέπει να δώσει στα request headers το Authorization Key του όπως εμφανίζεται στο παρακάτω παράδειγμα: 
```JSON
"Authorization" : "aa1ea2e6-f86c-11ec-81e3-0242ac180003"
```

Ένα session διαρκεί μέχρι ο χρήστης να πραγματοποιήσει έξοδο από το σύστημα, ή το σύστημα να ακυρώσει το session.


### Authorization Header Missing
Σε περίπτωση που ένας χρήστης ή διαχειριστής προσπαθήσει να χρησιμοποιήσει endpoint το οποίο απαιτεί authorization και λείπει το header, το σύστημα θα επιστρέψει το παρακάτω response :
```JSON
"Authorization key is missing. Please pass session_id in Authorization header."
```
Παράδειγμα λειτουργίας : https://prnt.sc/pbOG-blJyy9h


### No active session for provided key
Σε περίπτωση που ένας χρήστης ή διαχειριστής προσπαθήσει να χρησιμοποιήσει endpoint και το ***Authorization Key*** του δεν εντοπιστεί στα active sessions θα εμφανιστεί το παρακάτω μήνυμα : 
```JSON
"No active session. Please login"
```
Παράδειγμα λειτουργίας : https://prnt.sc/vOnUo4Su9XLr


### Permissions 
Για την χρήση των Endpoints υπάρχουν δύο ειδών εξουσιοδοτήσεις : 
- Required Permissions : Admin
- Required Permissions : Users

Οι χρήστες μπορούν να χρησιμοποιήσουν μόνο τα endpoints που απαιτούν Users permissions, ενώς οι admin αντίστοιχα μπορούν να χρησιμοποιήσουν μόνο τα endpoints που απαιτούν Admin permissions.

Σε περίπτωση που ένας χρήστης προσπαθήσει να χρησιμοποιήσει endpoints που απαιτούν admin permissions θα θα λάβει το παρακάτω Reponse :
```json
"This service is available only for admins."
```
Παράδειγμα λειτουργίας : https://prnt.sc/5u97Fu1uJ2Wv

Σε περίπτωση που ένας διαχειριστής προσπαθήσει να χρησιμοποιήσει endpoints που απαιτούν users permissions θα λάβει το παρακάτω Reponse :
```json
"This service is available only for simples users."
```
Παράδειγμα λειτουργίας : https://prnt.sc/7NVSux9lEB0T

## Εγγραφή στο σύστημα (Register)

Οι ενδιαφερόμενοι χρήστες μπορούν να πραγματοποιήσουν την εγγραφή τους στο πληροφοριακό σύστημα.

**Endpoint**
<pre>
<b>POST</b> /register
</pre>

*Authorization required* : **No**<br/>
*Permissions required* : **None**

**Request Body Schema**
```json
{
	"email" : "sagoropoulos@gmail.com",
	"firstName" : "Stelios", 
	"surName" : "Agoropoulos",
	"password" : "pass"
}
```

Ένας χρήστης μπορεί να πραγματοποιήσει την εγγραφή του στο σύστημα, ώστε να μπορεί στη συνέχεια να χρησιμοποιεί τις διαθέσιμες υπηρεσίες.
Για να μπορέσει ο χρήστης να πραγματοποιήσει με επιτυχία την εγγραφή του, είναι απαραίτητο να εισάγει τα παρακάτω στοιχεία : 
- Email
- Κωδικό πρόσβασης (password)
- Όνομα
- Επώνυμο

***Θεωρούμε ότι το username του χρήστη είναι το email του.***

Αν τα στοιχεία που δόθηκαν είναι σωστά και το email(username) δεν ανιτστοιχεί σε κάποιον άλλον χρήστη τότε η εγγραφή θα πραγματοποιηθεί με επιτυχία.
Σε περίπτωση που το σύστημα εντοπίσει ότι το email που δόθηκε αντιστοιχεί σε κάποιον χρήστη, θα επιστρέψει κατάλληλο μήνυμα.

### Παραδείγματα εκτέλεσης

Επιτυχής εγγραφή : https://prnt.sc/IhadTq4GkTk3

Το Request Body δεν καλύπτει το Required Schema: https://prnt.sc/Nb6yqjyvGU8o

Το email αντιστοιχεί σε άλλον χρήστη : https://prnt.sc/2D5u6oayh9_e


## Είσοδος στο σύστημα (Login)

Οι εγγεγραμμένοι χρήστες μπορούν να πραγματοποιήσουν την είσοδό τους στο πληροφοριακό σύστημα.

**Endpoint**
<pre>
<b>POST</b> /login
</pre>

*Authorization required* : **No**<br/>
*Permissions required* : **None**


**Request Body Schema**
```json
{
	"email" : "sagoropoulos@gmail.com",
	"password" : "pass", 
}
```

**Απλός χρήστης**<br/>
Ο χρήστης εφόσον έχει πραγματοποιήσει την εγγραφή του, μπορεί να κάνει απόπειρα εισόδου στο σύστημα.
Σε περίπτωση που το email δεν αντιστοιχεί σε κάποιον χρήστη, η υπηρεσία θα ενημερώσει με κατάλληλο μήνυμα.
Επίσης, αν ο κωδικός είναι λάθος, τότε το endpoint θα επιστρέψει το αντίστοιχο μήνυμα.

Σε περίπτωση που τα στοιχεία που δώσει είναι σωστά (email & κωδικός), τότε
θα εισέλθει επιτυχώς στο σύστημα, θα ενημερωθεί κατάλληλα και το σύστημα θα του επιστρέψει το ***session_id*** του, ώστε να μπορεί να το χρησιμοποιεί για το Authorization του στις 
υπόλοιπες υπηρεσίες του συστήματος.

**Διαχειριστής**<br/>
Για την είσοδο ενός διαχειριστή, ισχύουν τα παραπάνω που αφορούν και τους απλούς χρήστες. Επιπλέον όμως, όταν ένας διαχειριστής κάνει είσοδο στο σύστημα για πρώτη φορά, θα του ζητηθεί να 
αλλάξει τον προσωρινό κωδικό του. Σε περίπτωση που δεν τον αλλάξει και συνδεθεί ξανά (και ας μην είναι η πρώτη φορά), θα γίνει εκ νέου υπενθύμιση για αλλαγή κωδικού.
Η υπενθύμιση θα σταματήσει να εμφανίζεται, όταν ο διαχειριστής αλλάξει τον προσωρινό κωδικό του.

Παρακάτω δίνονται δύο Demo Accounts.

#### User Demo Login

email: sagoropoulos@gmail.com

password : 12345


#### Admin Demo Login

email : admin@infosys.gr

password : 123

### Παραδείγματα εκτέλεσης

Το Request Body δεν καλύπτει το Required Schema : https://prnt.sc/RTl9Ld99SSO9

Επιτυχής είσοδος : https://prnt.sc/M79Cf9B-tfYX

Λανθασμένος κωδικός : https://prnt.sc/Oyi_8M2ag3Uc

Υπάρχει ήδη ενεργή σύνδεση : https://prnt.sc/VsEIBkV1DfoD

Δεν υπάρχει ο χρήστης : https://prnt.sc/4GrKpLJKTUh-


## Αλλαγή κωδικού (Password Reset)
Οι χρήστες και οι διαχειριστές μπορούν να αλλάξουν τον κωδικό πρόσβασης τους.

**Endpoint**
<pre>
<b>PUT</b> /passwordReset
</pre>

*Authorization required* : **Yes**<br/>
*Permissions required* : **Admin or User**

**Required Headers**
```js
{
	"Authorization" : session_id (provided by system after succesful login)
}
```

**Request Body Schema**
```json
{
	"oldPass" : "1234",
	"newPass" : "123456", 
	"confirmPass" : "123456",
}
```

Για την επιτυχή αλλαγή του κωδικού, θα πρέπει: 
1. Το request body να καλύπτει το παραπάνω Required Schema.
2. ο παλιός κωδικός του χρήστη στο σύστημα να είναι ίδιος με αυτόν που έχει δώσει στο request του
3. ο παλιός κωδικός του body να διαφέρει από τον νέο κωδικό
4. ο νέος κωδικός να είναι ίδιος με το password confirmation.

Σε οποιαδήποτε περίπτωση λάθους, το σύστημα επιστρέφει κατάλληλο μήνυμα. Μόλις η διαδικασία ολοκληρωθεί με επιτυχία, το σύστημα κάνει αυτόματα logout τον χρήστη, του επιστρέφει μήνυμα επιτυχίας και του ζητάει να συνδεθεί ξανά.

### Παραδείγματα εκτέλεσης

To Request Body δεν καλύπτει το Required Schema: https://prnt.sc/eZpZruvgxrU_

Ο κωδικός στο σύστημα διαφέρει με αυτόν του request: https://prnt.sc/Ciq0etmF91Tz

Ο παλιός κωδικός είναι ίδιος με το νέο: https://prnt.sc/MpXHRT81QFYc

Ο νέος κωδικός δεν ταιριάζει με την επιβεβαίωση: https://prnt.sc/Gq5Eew4R_h55

Επιτυχής αλλαγή κωδικού: https://prnt.sc/uxtZITCvGOI6

## Έξοδος από το σύστημα (Logout)

Οι χρήστες μπορούν να αποσυνδεθούν από τον λογαριασμό τους.

**Endpoint**
<pre>
<b>POST</b> /logout
</pre>

*Authorization required* : **Yes**<br/>
*Permissions required* : **Admin or User**

**Required Headers**
```js
{
	"Authorization" : session_id (provided by system after succesful login)
}
```

Σε περίπτωση που ένας χρήστης θέλει να πραγματοποιήσει έξοδο από το σύστημα, μπορεί να χρησιμοποιήσει το συγκεκριμένο endpoint.</br>

Το σύστημα εντοπίζει τον χρήστη από το authorization key του και προσπαθεί να τον αποσυνδέσει από το σύστημα. Αν ο χρήστης δεν έχει πραγματοποιήσει είσοδο στο σύστημα και προσπαθήσει να κάνει logout θα του εμφανιστεί το κατάλληλο μήνυμα. </br>
Σε περίπτωση που η έξοδος από το σύστημα πραγματοποιηθεί με επιτυχία, ο χρήστης θα ενημερωθεί αντίστοιχα.


### Παραδείγματα εκτέλεσης

Επιτυχής αποσύνδεση: https://prnt.sc/7YzdG1N3YRhd

Ο χρήστης δεν είχε κάνει login: https://prnt.sc/YjzypHxQZgjo


## Διαγραφή λογαριασμού & δεδομένων (Delete Account)

Διαγραφή του λογαριασμού και των δεδομένων του από έναν χρήστη.

**Endpoint**
<pre>
<b>DELETE</b> /deleteAccount
</pre>

*Authorization required* : **Yes**<br/>
*Permissions required* : **User**

**Required Headers**
```json
{
	"Authorization" : session_id (provided by system after succesful login)
}
```

Ένας χρήστης μπορεί να πραγματοποιήσει διαγραφή του λογαριασμού και των δεδομένων του..
Το σύστημα αναγνωρίζει τον χρήστη βάσει του ***Authorization Key*** του και προχωράει στην διαγραφή του λογαριασμού του από την βάση καθώς και όλων των δεδομένων του και επιστρέφει το κατάλληλο μήνυμα.

### Παραδείγματα εκτέλεσης

Επιτυχής διαγραφή χρήστη και δεδομένων : https://prnt.sc/rJg2ufCugFDv


## Δημιουργία σημείωσης (Add Note)

Ένας χρήστης μπορεί δημιουργήσει μια σημείωση.

**Endpoint**
<pre>
<b>POST</b> /notes/add
</pre>

*Authorization required* : **Yes**<br/>
*Permissions required* : **User**

**Required Headers**
```json
 {
	"Authorization" : session_id (provided by system after succesful login)
}
```

**Request Body Schema**
```json
{
	"title" : "My first note!",
	"content" : "This is a dummy note.", 
	"tags" : "Tag1,Tag2,Tag3"
}
```

Ένας χρήστης μπορεί να δημιουργήσει μια σημείωση, ώστε να μπορεί στην συνέχεια να την βρει στο σύστημα.
Για την δημιουργία μιας είναι απαραίτητο να εισάγει τα παρακάτω στοιχεία : 
- Τίτλος
- Περιεχόμενο
- Λέξεις κλειδιά (tags) οι οποίες θα είναι χωρισμένες με κόμμα 

Σε περίπτωση που το request body δεν καλύπτει το απαιτούμενο schema όπως περιγράφεται παραπάνω, το σύστημα δεν θα προχωρήσει στην δημιουργία σημείωσης και θα επιστρέψει κατάλληλο μήνυμα.
Αν το request body περιέχει όλα τα απαραίτητα στοιχεία, η σημείωση θα δημιουργηθεί και θα επιστραφεί το αντίστοιχο μήνυμα.

### Παραδείγματα εκτέλεσης

To Request Body δεν καλύπτει το Required Schema: https://prnt.sc/hLmmGQco3HFz

Επιτυχής δημιουργία σημείωσης: https://prnt.sc/vSqCHepD1uT1


## Αναζήτηση σημείωσης με τίτλο (Search Note by Title)


Αναζήτηση σημείωσης βάσει του τίτλου της.

**Endpoint**
<pre>
<b>POST</b> /notes/search/<b>{title}</b>
</pre>

**Parameters:**
| Name | Type | Description |
| :----- |  :----- | :----- |
| title | String | A string with note's title. | 

*Authorization required* : **Yes**<br/>
*Permissions required* : **User**

**Required Request Headers**
```json
{
	"Authorization" : session_id (provided by system after succesful login)
}
```

Ένας χρήστης μπορεί να αναζητήσει μια ή περισσότερες σημειώσεις βάσει τίτλου.
Με αυτό τον τρόπο θα μπορέσει να πάρει και το μοναδικό ID της κάθε σημείωσης, ώστε στη συνέχεια να μπορέσει να πραγματοποιήσει επιπλέον ενέργειες (update, delete etc.).
Για την αναζήτηση της σημείωσης θα πρέπει ο χρήστης στο endpoint να δώσει και τον τίτλο της σημείωσης.
Στη συνέχεια το σύστημα θα επιστρέψει όλες τις σημειώσεις που έχουν τον τίτλο που δόθηκε. Σε περίπτωση που δεν υπάρχει σημείωση, θα επιστραφεί κενό.

### Παραδείγματα εκτέλεσης

Επιτυχία εύρεσης σημείωσης/σημειώσεων : https://prnt.sc/yhvv32TerrvA

Αποτυχία εύρεσης σημείωσης/σημειώσεων : https://prnt.sc/8XXlPlOONzI1


## Αναζήτηση σημείωσης με λέξει κλειδί (Search Note by Tag)

Αναζήτηση των σημειώσεων που περιέχουν μια συγκεκριμένη λέξη κλειδί.

**Endpoint**
<pre>
<b>POST</b> /notes/searchByTag/<b>{tag}</b>
</pre>

**Parameters:**
| Name | Type | Description |
| :----- |  :----- | :----- |
| tag | String | A string with tag you want to search. | 

*Authorization required* : **Yes**<br/>
*Permissions required* : **User**

**Required Headers**
```json
{
	"Authorization" : session_id (provided by system after succesful login)
}
```

Ένας χρήστης μπορεί να αναζητήσει μια ή περισσότερες σημειώσεις βάσει μιας λέξης κλειδί.
Για την αναζήτηση της σημείωσης θα πρέπει ο χρήστης στο endpoint να δώσει και την λέξη κλειδί για την οποία θέλει να πραγματοποιήσει την αναζήτηση.
Στη συνέχεια το σύστημα θα επιστρέψει όλες τις σημειώσεις που περιέχουν την ζητούμενη λέξη κλειδί **σε φθίνουσα σειρά βάσει της ημερομηνίας δημιουργίας** (πιο πρόσφατες προς πιο παλιές). Σε περίπτωση που δεν υπάρχει σημείωση που να ικανοποιεί την αναζήτησή, θα επιστραφεί κατάλληλο μήνυμα.

### Παραδείγματα εκτέλεσης

Επιτυχία εύρεση σημείωσης/σημειώσεων :  https://prnt.sc/3mjnP4yKVWp-

Αποτυχία εύρεσης σημείωσης/σημειώσεων : https://prnt.sc/kT_A906CAh81



## Διόρθωση/αλλαγή υπάρχουσας σημείωσης (Update note)

Διόρθωση/αλλαγή των πεδίων μιας υπάρχουσαν σημείωσης.

**Endpoint**
<pre>
<b>PATCH</b> /notes/update/<b>{id}</b>
</pre>

**Parameters:**
| Name | Type | Description |
| :----- |  :----- | :----- |
| id | hex | Note's id. Provided by "Search by Title" endpoint. | 

*Authorization required* : **Yes**<br/>
*Permissions required* : **User**

**Required Headers**
```json
{
	"Authorization" : session_id (provided by system after succesful login)
}
```

**Request Body Example 1**
```json
 {
	"title" : "My first note!",
	"content" : "This is a dummy note.", 
}
```

**Request Body Example 2**
```json
 {
	"tags" : "Tag1,Tag2,Tag3"
}
```

Ένας χρήστης μπορεί να πραγματοποιήσει αλλαγή σε **οποιαδήποτε** από τις τρείς παρακάτω τιμές μιας σημείωσης: 
- Τίτλος σημείωσης
- Περιεχόμενο
- Λέξεις κλειδιά

Για την εύρεση και διόρθωση της σημείωσης που επιθυμεί ο χρήστης **θα πρέπει στο endpoint να δώσει το id** (μπορεί να το βρει από το "Search by Title" endpoint).
Σε περίπτωση που δεν βρεθεί σημείωση με το δοθέν id, τότε το σύστημα θα επιστρέψει και πάλι στον χρήστη το κατάλληλο μήνυμα.
Στη συνέχεια θα πρέπει να πραγματοποιήσει ένα request που να περιέχει τουλάχιστον ένα από τα τρια πεδία.Αν το Request Body δεν περιέχει κανένα από τα τρία πεδία, τότε το σύστημα θα επιστρέψει το κατάλληλο μήνυμα λάθους.
Αν η διαδικασία ολοκληρωθεί κανονικά, εμφανίζεται μήνυμα επιτυχίας.

### Παραδείγματα εκτέλεσης

Το id δεν είναι valid(hex or 24digit)) : https://prnt.sc/7fLAVwQiQLet

Το Request Body δεν καλύπτει το schema : https://prnt.sc/7wqMLuLtpy3u

Η σημείωση έγινε update με επιτυχία : https://prnt.sc/ojho-_Nf1U1k

Δεν βρέθηκε η σημείωση που ζητήθηκε : https://prnt.sc/AUcmx-73jUia


## Διαγραφή σημείωσης (Delete note)

Διαγραφή μιας σημείωσης του χρήστη από το σύστημα.

**Endpoint**
<pre>
<b>DELETE</b> /notes/delete/<b>{id}</b>
</pre>

**Parameters:**
| Name | Type | Description |
| :----- |  :----- | :----- |
| id | 24-digit hex | Note's id. Provided by "Search by Title" endpoint. | 

*Authorization required* : **Yes**<br/>
*Permissions required* : **User**

**Required Headers**
```json
{
	"Authorization" : session_id (provided by system after succesful login)
}
```

Ένας χρήστης μπορεί να πραγματοποιήσει διαγραφή μιας σημείωσης του.
Για την εύρεση και διαγραφή της σημείωσης που επιθυμεί ο χρήστης **θα πρέπει στο endpoint να δώσει το id** (μπορεί να το βρει από το "Search by Title" endpoint).
Σε περίπτωση που δεν βρεθεί σημείωση με το δοθέν id, τότε το σύστημα θα επιστρέψει και πάλι στον χρήστη το κατάλληλο μήνυμα.
Αν η διαδικασία ολοκληρωθεί κανονικά, εμφανίζεται μήνυμα επιτυχίας.

### Παραδείγματα εκτέλεσης

Το id δεν είναι valid(24-digit hex) : https://prnt.sc/Dx7Itj3NCA1o

Δεν βρέθηκε η σημείωση που ζητήθηκε : https://prnt.sc/yNcSj6yxaGSz

Η σημείωση διαγράφηκε με επιτυχία : https://prnt.sc/_mGmB_I4evcf


## Εύρεση όλων των σημειώσεων του χρήστη (Get All Notes)

Εύρεση όλων των σημειώσεων που έχει δημιουργήσει ο χρήστης.

**Endpoint**
<pre>
<b>GET</b> /notes/getAll/<b>{sortType}</b>
</pre>

**Parameters:**
| Name     |  Type     |   Values  |                Description                        |
| :-----   |  :-----   |  :-----   | :----- 											  |
| sortType |  String   | asc, desc | Note's id. Provided by "Search by Title" endpoint.|

*Authorization required* : **Yes**<br/>
*Permissions required* : **User**

**Required Headers**
```json
{
	"Authorization" : session_id (provided by system after succesful login)
}
```

Ένας χρήστης μπορεί να πραγματοποιήσει αναζήτηση όλων των σημειώσεων του.
Είναι απαραίτητο ο χρήστης να επιλέξει την χρονολογική σειρά με την οποία θα εμφανίζονται οι σημειώσεις τους, δίνοντας το κατάλληλο parameter. Οι επιλογές είναι οι εξής : 
- asc : ASCENDING->ταξινόμηση από την πιο παλιά προς τις νεότερες
- desc : DESCENDING -> ταξινόμηση από τις νεότερες προς τις πιο παλιές

Σε περίπτωση που δεν βρεθούν σημειώσεις, το σύστημα θα επιστρέψει ένα κενό payload. Διαφορετικά θα επιστρέψει όλες τις σημειώσεις του χρήστη, ταξινομημένες σύμφωνα με την επιλογή του.

### Παραδείγματα εκτέλεσης

Λάθος parameter ***sortType*** : https://prnt.sc/ZxIbVxO5SkY9 

Δεν βρέθηκαν σημειώσεις :  

Επιτυχής εύρεση σημειώσεων σε αύξουσα σειρά : https://prnt.sc/mZOnXeFHIh_T

Επιτυχής εύρεση σημειώσεων σε φθίνουσα σειρά : https://prnt.sc/cZgY6ZGh-lTd


## Εισαγωγή νέου διαχειριστή (Add Admin)

Ένας διαχειριστής μπορεί να εισάγει έναν νέο διαχειριστή στην υπηρεσία.

**Endpoint**
<pre>
<b>POST</b> /addAdmin
</pre>

*Authorization required* : **Yes**<br/>
*Permissions required* : **Admin**

**Required Headers**
```json
{
	"Authorization" : session_id (provided by system after succesful login)
}
```

**Request Body Schema**
```json
{
	"email" : "admin2@infosys.gr",
	"firstName" : "John", 
	"surName" : "Doe"
}
```

Ένας διαχειριστής μπορεί να εισάγει έναν νέο διαχειριστή στο σύστημα.
Για την εισαγωγή είναι απαραίτητα τα παρακάτω στοιχεία : 
- Email
- Όνομα
- Επώνυμο

Σε περίπτωση που το request body δεν καλύπτει το απαιτούμενο schema όπως περιγράφεται παραπάνω, το σύστημα δεν θα προχωρήσει στην δημιουργία του λογαριασμού διαχειριστή και θα επιστρέψει κατάλληλο μήνυμα.
Αν το Request body  γίνει αποδεκτό, γίνεται validation του email format. Σε περίπτωση που το format είναι λανθασμένο, εμφανίζεται αντίστοιχο μήνυμα.
Σε περίπτωση που το email που δόθηκε αντιστοιχεί σε κάποιον διαχειριστή, τότε θα εμφανιστεί και πάλι το κατάλληλο μήνυμα.
Μόλις όλοι οι έλεγχοι ολοκληρωθούν με επιτυχία δημιουργείται ο νέος λογαριασμός του διαχειριστή με έναν προσωρινό κωδικό και flag για password reset. 

### Παραδείγματα εκτέλεσης

Το Request Body δεν καλύπτει το schema : https://prnt.sc/SZCakDNdE2hH

To email είναι λανθασμένο : https://prnt.sc/ohOgWRqKMnXO

Υπάρχει ήδη διαχειριστής με αυτό το email : https://prnt.sc/eIhPd6qbYmW0

Επιτυχής εισαγωγή διαχειριστή : https://prnt.sc/QEMQpzXlo206


## Διαγραφή χρήστη (Delete user)

Οι διαχειριστές μπορούν να προχωρήσουν στην διαγραφή του λογαριασμού ενός χρήστη.

**Endpoint**
<pre>
<b>DELETE</b> /deleteUser<b>{email}</b>
</pre>

**Parameters:**
| Name | Type | Description |
| :----- |  :----- | :----- |
| email | String | User's email to delete account | 

*Authorization required* : **Yes**<br/>
*Permissions required* : **Admin**

**Required Headers**
```json
{
	"Authorization" : session_id (provided by system after succesful login)
}
```

Οι διαχειριστές μπορούν να προχωρήσουν στην διαγραφή του λογαριασμού ενός χρήστη.
Για την εύρεση και διαγραφή του λογαριασμού του χρήστης, ο διαχειριστής **θα πρέπει στο endpoint να δώσει σαν parameter το email του χρήστη** που επιθυμεί να διαγράψει.
Σε περίπτωση που δεν βρεθεί ο χρήστης με το δοθέν email/username, τότε το σύστημα θα επιστρέψει το κατάλληλο μήνυμα.
Αν η διαδικασία ολοκληρωθεί σωστά, επιστρέφεται μήνυμα επιτυχίας.

### Παραδείγματα εκτέλεσης

Επιτυχής διαγραφή ενός χρήστη : https://prnt.sc/zozYwCdhr0em

Ο χρήστης που ζητήθηκε να διαγραφεί δεν βρέθηκε : https://prnt.sc/ENrCch-GHeLg
