document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('adopterForm');
     /**
     * Valide un champ du formulaire en fonction de son ID et de sa valeur.
     * @param {HTMLElement} field - Le champ à valider.
     * @returns {boolean} - True si le champ est valide, false sinon.
     */
     function validerChamp(field) {
        const error = document.getElementById(`error-${field.id}`);
        let estValide = true;
        let msgErreur = '';

        if(!field.value){
            msgErreur = 'Erreur :  Tous les champs du formulaire sont obligatoires;';
            estValide = false;
        }

        if(field.value.includes(',')){
            msgErreur = 'Erreur : Aucun champ ne peut contenir une virgule. ';
            estValide = false;
        }

        switch (field.id) {
            case 'nom':
                if(field.value.length < 3 || field.value.length > 20){
                    msgErreur = 'Le nom de l\'animal doit avoir entre 3 et 20 caractères.';
                    estValide = false;
                }

                break;

            case 'age':
                const age = parseInt(field.value);
                if(isNaN(age) || age < 0 || age > 30){
                    msgErreur = 'L\'âge doit être une valeur numérique entre 0 et 30.';
                    estValide = false;

                }

                break;

            case 'courriel':
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if(!emailRegex.test(field.value)){
                    msgErreur = 'L\'adresse courriel doit avoir un format valide.';
                    estValide = false;
                }

                break;

            case 'cp':
                const cpRegex = /^[A-Z]\d[A-Z] \d[A-Z]\d$/;
                if(!cpRegex.test(field.value)){
                    msgErreur = ' Le code postal doit avoir un format canadien.';
                    estValide = false;
                }

                break;

        }

        error.style.display = estValide ? 'none' : 'block';
        error.textContent = msgErreur;

        return estValide;
    }

    // Validation en temps réel des champs du formulaire
    form.querySelectorAll('input, select').forEach(element => {
        element.addEventListener('change', function () {
            validerChamp(this);
        });
    });

})