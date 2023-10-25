document.getElementById("submitBtn").addEventListener("click", function () {
    var requiredFields = ["prenom", "nom", "mail", "telephone", "date_naissance", "lieu_naissance", "adresse", "num_secu_sociale", "conge_spectacle", "cni", "date_delivrance", "date_expiration", "carte_train"];

    var formIsValid = true;

    for (var i = 0; i < requiredFields.length; i++) {
        var fieldName = requiredFields[i];
        var fieldValue = document.getElementById(fieldName).value;

        if (fieldValue.trim() === "") {
            formIsValid = false;
            document.getElementById(fieldName).style.border = "1px solid red";
        } else {
            document.getElementById(fieldName).style.border = "1px solid #ccc";
        }
    }

    if (formIsValid) {
        if (confirm("Voulez-vous envoyer votre formulaire ?")) {
            document.getElementById("myForm").submit();
        }
    }
});
