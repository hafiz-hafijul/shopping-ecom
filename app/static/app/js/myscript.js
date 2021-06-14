$("#slider1, #slider2, #slider3,#slider4").owlCarousel({
  loop: true,
  margin: 20,
  responsiveClass: true,
  responsive: {
    0: {
      items: 1,
      nav: false,
      autoplay: true,
    },
    600: {
      items: 3,
      nav: true,
      autoplay: true,
    },
    1000: {
      items: 5,
      nav: true,
      loop: true,
      autoplay: true,
    },
  },
});

$(".plus-cart").click(function () {
  let id = $(this).attr("pid").toString();
  let em = this.parentNode.children[2];
  let am = document.getElementById("amount");
  let ttam = document.getElementById("totalamount");

  $.ajax({
    type: "GET",
    url: "/pluscart",
    data: {
      prod_id: id,
    },
    success: function (data) {
      em.innerText = data.quantity;
      am.innerText = data.amount;
      ttam.innerText = data.totalamount;
    },
  });
});

$(".minus-cart").click(function () {
  let id = $(this).attr("pid").toString();
  let em = this.parentNode.children[2];
  let am = document.getElementById("amount");
  let ttam = document.getElementById("totalamount");

  $.ajax({
    type: "GET",
    url: "/minuscart",
    data: {
      prod_id: id,
    },
    success: function (data) {
      em.innerText = data.quantity;
      am.innerText = data.amount;
      ttam.innerText = data.totalamount;
    },
  });
});

$(".remove-cart").click(function () {
  let id = $(this).attr("pid").toString();
  let rm = this
  let am = document.getElementById("amount");
  let ttam = document.getElementById("totalamount");

  $.ajax({
    type: "GET",
    url: "/removecart",
    data: {
      prod_id: id,
    },
    success: function (data) {
      am.innerText = data.amount;
      ttam.innerText = data.totalamount;
      rm.parentNode.parentNode.parentNode.parentNode.remove();
    },
  });
});
