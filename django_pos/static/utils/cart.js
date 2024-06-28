function togglePlaySound() {
  // session storage is used to store the state of the sound - under AppSettings Session
  let settings = sessionStorage.getItem("AppSettings");
  let sound = settings ? JSON.parse(settings).play_sound : true;
  // toggle sound state
  sound = !sound;
  sessionStorage.setItem("AppSettings", JSON.stringify({ play_sound: sound }));

  return sound;
}

$(document).ready(function () {
  $("#sound_btn").on("click", function () {
    let sound = togglePlaySound();
    if (sound) {
      $(this).html('<i class="ti ti-volume hover-q text-muted" title=""></i>');
    } else {
      $(this).html(
        '<i class="ti ti-volume-off hover-q text-muted" title=""></i>'
      );
    }
  });
});

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }

  return cookieValue;
}
function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
}

// To avoid error 403 Forbidden
$.ajaxSetup({
  beforeSend: function (xhr, settings) {
    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
      xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    }
  },
});

let shoppingCart = (function () {
  let cart = [];

  // Constructor
  function Item(name, price, count, id) {
    this.name = name;
    this.price = price;
    this.count = count;
    this.id = id;
  }

  // Save cart
  function saveCart() {
    sessionStorage.setItem("shoppingCart", JSON.stringify(cart));
  }

  // Load cart
  function loadCart() {
    cart = JSON.parse(sessionStorage.getItem("shoppingCart"));
  }
  if (sessionStorage.getItem("shoppingCart") != null) {
    loadCart();
  }

  let obj = {};

  // Add to cart
  obj.addItemToCart = function (name, price, count, id) {
    for (let item in cart) {
      if (cart[item].name === name) {
        cart[item].count++;
        saveCart();
        return;
      }
    }
    let item = new Item(name, price, count, id);
    cart.push(item);
    saveCart();
  };
  // Set count from item
  obj.setCountForItem = function (name, count) {
    for (let i in cart) {
      if (cart[i].name === name) {
        cart[i].count = count;
        break;
      }
    }
    saveCart();
  };
  // Remove item from cart
  obj.removeItemFromCart = function (name) {
    for (let item in cart) {
      if (cart[item].name === name) {
        cart[item].count--;
        if (cart[item].count === 0) {
          cart.splice(item, 1);
        }
        break;
      }
    }
    saveCart();
  };

  // Remove all items from cart
  obj.removeItemFromCartAll = function (name) {
    for (let item in cart) {
      if (cart[item].name === name) {
        cart.splice(item, 1);
        break;
      }
    }
    saveCart();
  };

  // Clear cart
  obj.clearCart = function () {
    cart = [];
    saveCart();
  };

  // Count cart
  obj.totalCount = function () {
    let totalCount = 0;
    for (let item in cart) {
      totalCount += cart[item].count;
    }
    return totalCount;
  };

  // Total cart
  obj.totalCart = function () {
    let totalCart = 0;
    for (let item in cart) {
      totalCart += cart[item].price * cart[item].count;
    }
    return Number(totalCart.toFixed(2));
  };

  // List cart
  obj.listCart = function () {
    let products = [];
    for (let i in JSON.parse(sessionStorage.getItem("shoppingCart"))) {
      let item = cart[i];
      let product = {
        id: item.id,
        name: item.name,
        price: item.price,
        count: item.count,
        total: (item.price * item.count).toFixed(2),
      };
      products.push(product);
    }
    return products;
  };

  return obj;
})();
