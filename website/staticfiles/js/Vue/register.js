const registerContainerAts  = new Vue({
      delimiters: ['[[', ']]'],
      el: '#registerContainerAts',
      data: {
            // register
            showModalLogin: false,
            id_username: null,
            id_email: null,
            id_password1: null,
            id_password2: null,

            type:null,
            showFormPro: false,
            showFormPart: false,

            //general
            errors: [],
            success_msg: "",
            err_msg: "",
            serverSuccess: false,
            serverError: false,

      },
           mounted() {
            let inputs = document.getElementsByClassName("input");
            for (let i = 0; i < inputs.length; i++) {
                this.toggleInputContainer(inputs[i]);
            }
           },

      methods: {
          toggleFormPro(evt, ref) {
              ref.href = evt.target.dataset.url;
              this.showFormPro = !this.showFormPro;
              this.showFormPart = false;
          },
          toggleFormPart(evt, ref) {
              ref.href = evt.target.dataset.url;
              this.showFormPart = !this.showFormPart;
              this.showFormPro = false;
          },
          toggleInputs(evt) {
               this.toggleInputContainer(evt.target);
          },
          toggleLabels(evt){
            evt.target.previousElementSibling.focus();
          },
          toggleInputContainer(input){
            if (input.value != "") {
                input.classList.add('filled');
            } else {
                input.classList.remove('filled');
            }
        },
          switchVisibility(evt) {
              let input = evt.target.previousElementSibling.previousElementSibling;
              input.type = input.type === 'password' ? 'text' : 'password';
              evt.target.innerHTML === 'visibility' ? evt.target.innerHTML = 'visibility_off' : evt.target.innerHTML = 'visibility'
        },
      }
    });