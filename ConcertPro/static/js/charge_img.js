document.getElementById('image-input').addEventListener('change', function() {
    var fichier = this.files[0]; // Obtenir le premier fichier sélectionné
    if (fichier) {
        var img = document.getElementById('image-charge');
        img.src = URL.createObjectURL(fichier);
    }
});
