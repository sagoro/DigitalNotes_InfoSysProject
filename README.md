# YpoxreotikiErgasia22_e16001_Agoropoulos_Stelios
Εργασία εξαμήνου για το μάθημα "Πληροφοριακά Συστήματα" Εαρινό 2022 - Αγορόπουλος Στέλιος e16001


## Λειτουργίες συστήματος

### User Registration

Endpoint:
| Method | Resource | Description |
| :----- |  :----- | :----- |
| POST | /register | Register a user in the system. | 


Request Body Example: 
```json
 {
		"email" : "sagoropoulos@gmail.com", //Required field
		"firstName" : "Stelios", //Required field
		"surName" : "Agoropoulos", //Required field
		"password" : "pass" //Required field
		}
```