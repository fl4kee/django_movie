let html = '<% for (movie of movies) {%>\
            <div class="col-md-4 product-men">\
            <div class="product-shoe-info editContent text-center mt-lg-4">\
                <div class="men-thumb-item">\
                    <img src="media/<%= movie.poster %>" class="img-fluid" alt="">\
                </div>\
                <div class="item-info-product">\
                    <h4 class="">\
                        <a href="/<%= movie.url %>" class="editContent"><%= movie.title %></a>\
                    </h4>\
                    <div class="product_price">\
                        <div class="grid-price">\
                            <span class="money editContent"><%= movie.tagline %></span>\
                        </div>\
                    </div>\
                    <ul class="stars">\
                        <li><a href="#"><span class="fa fa-star" aria-hidden="true"></span></a></li>\
                        <li><a href="#"><span class="fa fa-star" aria-hidden="true"></span></a></li>\
                        <li><a href="#"><span class="fa fa-star-half-o" aria-hidden="true"></span></a>\
                        </li>\
                        <li><a href="#"><span class="fa fa-star-half-o" aria-hidden="true"></span></a>\
                        </li>\
                        <li><a href="#"><span class="fa fa-star-o" aria-hidden="true"></span></a></li>\
                    </ul>\
                </div>\
            </div>\
        </div>\
        <% } %>'

function render(data){
    //Рендер шаблона
    let output = ejs.render(html, data);
    console.log(data)

    const div = document.querySelector('.left-ads-display>.row')
    div.innerHTML = output;
}

function ajaxSend(url, params){
    // Отправляем запрос
    fetch(`${url}?${params}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    })
        .then(response => response.json())
        .then(json => render(json))
        .catch(error => console.error(error))
}

//const forms = document.querySelector('form[name=filter]');
//
//forms.addEventListener('submit', function(e) {
//    e.preventDefault();
//    let url = this.action;
//    let params = new URLSearchParams(new FormData(this)).toString();
//    ajaxSend(url, params)
//})

const rating = document.querySelector('form[name=rating]');

rating.addEventListener('change', function(e) {
    let data = new FormData(this);
    fetch(`${this.action}`, {
        method: 'POST',
        body: data
    })
        .then(response => alert("Рейтинг установлен"))
        .catch(error => alert("Ошибка"))
})