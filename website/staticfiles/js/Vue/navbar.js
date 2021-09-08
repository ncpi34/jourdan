const navbar  = new Vue({
      delimiters: ['[[', ']]'],
      el: '#navbarVue',
      data: {
            // navbar
            hoverNavbar: false,
            onClickSideNav: false,
            showSidenav: false,
            showOption: false,
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
            rowHover: -1,

            cartItemsNumber: 0

      },
        computed: {
          navState() {
              return this.showSidenav ? 'slide-left' : '';
            }
        },
        mounted(){

            //get local storage value on event
            window.addEventListener('cartLengthLocalstorageChanged', (event) => {
                this.cartItemsNumber = event.detail.storage;
            });
        },
      methods: {
          toggleOption(){
              this.showOption = !this.showOption;

            //animation on open
              if(this.showOption){
                  this.$refs.hamburger.classList.add("animate-spin");

                  setTimeout( () => {
                      this.$refs.hamburger.classList.remove("animate-spin");
                  }, 500);
              }

              setTimeout( () => {
                  this.showOption ? this.$refs.hamburger.innerHTML = 'clear' : this.$refs.hamburger.innerHTML = 'menu';
              }, 10)





        }

      }
    });