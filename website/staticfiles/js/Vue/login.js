 const login  = new Vue({
      delimiters: ['[[', ']]'],
      el: '#loginVue',
      data: {

            errors: [],
            loading: false,

            // forgot pwd
            showModalForgotPwd: false,
            email: null,

            //general
            success_msg: "",
            err_msg: "",
            currentURL: window.location.href,
            serverSuccess: false,
            serverError: false,
            toggleDynamicMenu: null,
            toggleHoverMenus: null,
            rowHover: -1

      },
     methods: {
          // forgot pwd
          toggleModalForgotPwd: function(){
              this.showModalLogin = false;
               this.showModalForgotPwd = !this.showModalForgotPwd;
        },
          checkFormForgotPwd(e) {
              let url = e.target.dataset.url;
              let token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
              if (this.email ) {
                  this.loading = true;
                 this.forgotPwd(url, token).then(response => {
                    this.serverSuccess = true;
                    this.success_msg = response.data['msg'];
                    this.redirectAfterSuccess();
                  }).catch(err => {
                      this.loading = false;
                      this.serverError = true;
                      this.err_msg = err.response.data['err'];
                      setTimeout(() => {
                          this.serverError = false;
                      }, 2000)
                  });
              }

              if (!this.email) {
                this.errors.push('Email requis');
              }

              if (!this.errors.length) {
                  e.target.reset(); // reset form
                  return true;
              }


            },
          async forgotPwd(url, token) {
            this.success_msg = "";
                this.err_msg = "";
            return await axios({
                    method : "POST",
                    url:url, //django path name
                    headers: {'X-CSRFTOKEN': token, 'Content-Type': 'application/json'},
                    data : {"forgot_pass_email":this.email},//data
                  })
          },
          redirectAfterSuccess() {
              setTimeout(() => {
                  //window.location.href = this.currentURL;
                  //window.location.replace(this.currentURL);
                  window.location.assign(this.currentURL);
                  // window.location.replace(this.currentURL);
              }, 2000);

          }

      }
    });