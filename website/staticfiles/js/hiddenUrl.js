// to insert path in hidden form
if (document.querySelectorAll('.btn_send')) {
    let btn_send = document.querySelectorAll('.btn_send');
        let hidden_url = document.querySelectorAll('.url_to_redirect_after_cart_add');
        for (const button of btn_send) {
          button.addEventListener('click', () => {
              hidden_url.forEach(val => {
                  val.value=window.location.href;
                  // val.value=window.location.pathname;
              })
          })

        }
}
