

function signup() {
    let name = $("#name").val();
    let email = $("#email").val();
    let password = $("#password").val();

    if (name == '' || email == '' || password == '') {
        Swal.fire(
            'Oops',
            'Data tidak lengkap!',
            'error'
        )
    } else {
        $.ajax({
            type: "POST",
            url: "/sign_up/save",
            data: {
                name: name,
                email: email,
                password: password
            },
            success: function (response) {
                Swal.fire(
                    'Done',
                    'You are signed up, nice!',
                    'success'
                )
                window.location.replace("/signin");
            },
        });
    }


}
function sign_in() {
    let email = $("#email").val();
    let password = $("#password").val();

    $.ajax({
        type: "POST",
        url: "/sign_in",
        data: {
            email: email,
            password: password,
        },
        success: function (response) {
            if (response["result"] === "success") {
                $.cookie("mytoken", response["token"], { path: "/" });
                window.location.replace("/");
            } else {
                // alert(response["msg"]);
                Swal.fire(
                    'Oops',
                    response["msg"],
                    'error'
                )
            }
        },
    });
}

function admin_signup() {
    let name = $("#name").val();
    let email = $("#email").val();
    let password = $("#password").val();

    if (name == '' || email == '' || password == '') {
        Swal.fire(
            'Oops',
            'Data tidak lengkap!',
            'error'
        )
    } else {
        $.ajax({
            type: "POST",
            url: "/sign_up/admin",
            data: {
                name: name,
                email: email,
                password: password
            },
            success: function (response) {
                Swal.fire(
                    'Done',
                    'You are signed up, nice!',
                    'success'
                )
                window.location.replace("/signin/admin");
            },
        });
    }


}
function admin_sign_in() {
    let email = $("#email").val();
    let password = $("#password").val();

    $.ajax({
        type: "POST",
        url: "/sign_in/admin",
        data: {
            email: email,
            password: password,
        },
        success: function (response) {
            if (response["result"] === "success") {
                $.cookie("mytoken", response["token"], { path: "/" });
                window.location.replace("/home_admin");
            } else {
                // alert(response["msg"]);
                Swal.fire(
                    'Oops',
                    response["msg"],
                    'error'
                )
            }
        },
    });
}

function sign_out() {
    $.removeCookie("mytoken", { path: "/" });
    alert("Logged out!");
    window.location.href = "/";
    // Swal.fire({
    //     icon: 'success',
    //     title: 'Logged Out!',
    //     text: 'You have been successfully logged out.',
    //     showConfirmButton: false,
    //     timer: 2000, // Adjust the timer value (in milliseconds) as needed
    //     onClose: function() {
    //         window.location.reload();
    //     }
    // });
}

function submit() {
    let nama = $("#nama").val();
    let email = $("#email").val();
    let phone = $("#phone").val();
    let pesan = $("#pesan").val();

    if (nama == '' || email == '' || phone == '' || pesan == '') {
        Swal.fire(
            'Oops',
            'Data tidak lengkap!',
            'error'
        )
    } else {
    $.ajax({
        type: "POST",
        url: "/contact/save",
        data: {
            nama: nama,
            email: email,
            phone: phone,
            pesan: pesan,
        },
        success: function (response) {
            Swal.fire(
                'Done',
                'You are signed up, nice!',
                'success'
            )
            window.location.replace("/contact");
            },
        });
    }
}

function openModal() {
    const modal = document.getElementById('modal');
    modal.classList.add('is-active');
}

function closeModal() {
    const modal = document.getElementById('modal');
    modal.classList.remove('is-active');
    modal.classList.add('is-closing');

    setTimeout(function () {
        modal.classList.remove('is-closing');
    }, 300);
}


