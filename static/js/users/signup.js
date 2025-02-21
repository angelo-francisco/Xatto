class UnicodeUsernameValidator {
    constructor() {
        this.regex = /^[\w.]+$/;
        this.errorMessage = "Este username é inválido";
    }

    validate(username) {
        if (!this.regex.test(username)) {
            throw new Error(this.errorMessage);
        }
        return true;
    }

    async is_valid(username) {
        try {
            const response = await fetch(`/auth/check-username/${username}`);
            const data = await response.json();
            return data.status;
        } catch (error) {
            console.error("Erro ao verificar o nome de usuário:", error);
            return null;
        }
    }

}

let submitBtn = document.querySelector(".submit-btn")

document.getElementById('username')
    .addEventListener('keyup', (event) => {
        const username = event.target.value.trim();
        let validator = new UnicodeUsernameValidator();
        let span = document.getElementById('username-span')

        if (username.length == 0) {
            span.textContent = ''
            submitBtn.disabled = true
            submitBtn.classList.add('disabled')
            return;
        }

        try {
            validator.validate(username);

            span.innerHTML = ''
            submitBtn.disabled = false
            submitBtn.classList.remove('disabled')
        } catch (error) {
            span.innerHTML = `
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x-circle" viewBox="0 0 16 16">
                        <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/>
                        <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708"/>
                    </svg>
                    &nbsp;${error.message}
                `
            span.style.color = 'red';
            submitBtn.disabled = true
            submitBtn.classList.add('disabled')
            return;
        }

        try {
            validator.is_valid(username)
                .then(status => {
                    if (status) {
                        span.innerHTML = `
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                                    class="bi bi-check2-circle" viewBox="0 0 16 16">
                                    <path
                                        d="M2.5 8a5.5 5.5 0 0 1 8.25-4.764.5.5 0 0 0 .5-.866A6.5 6.5 0 1 0 14.5 8a.5.5 0 0 0-1 0 5.5 5.5 0 1 1-11 0" />
                                    <path
                                        d="M15.354 3.354a.5.5 0 0 0-.708-.708L8 9.293 5.354 6.646a.5.5 0 1 0-.708.708l3 3a.5.5 0 0 0 .708 0z" />
                            </svg>
                            &nbsp;Username disponível
                            `
                        span.style.color = 'green'
                        submitBtn.disabled = false
                        submitBtn.classList.remove('disabled')
                    }
                    else {
                        span.innerHTML = `
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x-circle" viewBox="0 0 16 16">
                                    <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/>
                                    <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708"/>
                                </svg>
                                &nbsp;Username não está disponível
                            `
                        span.style.color = 'red'
                        submitBtn.disabled = true
                        submitBtn.classList.add('disabled')
                        return;
                    }
                })
        } catch (error) {
            console.log(error)
        }
    })

class EmailValidator {
    constructor() {
        this.regex = /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/;
        this.errorMessage = "E-mail inválido";
    }

    validate(email) {
        if (!this.regex.test(email)) {
            throw new Error(this.errorMessage);
        }
        return true;
    }

    async is_valid(email) {
        try {
            const response = await fetch(`/auth/check-email/${email}`);
            const data = await response.json();
            return data.status;
        } catch (error) {
            console.error("Erro ao verificar o nome de usuário:", error);
            return null;
        }
    }
}

document.getElementById('email')
    .addEventListener('keyup', (event) => {
        const email = event.target.value.trim();
        let validator = new EmailValidator();
        let span = document.getElementById('email-span')

        if (email.length == 0) {
            span.textContent = ''
            submitBtn.disabled = true
            submitBtn.classList.add('disabled')
            return;
        }

        try {
            validator.validate(email);

            span.innerHTML = ''
            submitBtn.disabled = false
            submitBtn.classList.remove('disabled')
        } catch (error) {
            span.innerHTML = `
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x-circle" viewBox="0 0 16 16">
                        <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/>
                        <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708"/>
                    </svg>
                    &nbsp;${error.message}
                `
            span.style.color = 'red';
            submitBtn.disabled = true
            submitBtn.classList.add('disabled')
            return;
        }

        try {
            validator.is_valid(email)
                .then(status => {
                    if (status) {
                        span.innerHTML = ''
                        submitBtn.disabled = false
                        submitBtn.classList.remove('disabled')
                    }
                    else {
                        span.innerHTML = `
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x-circle" viewBox="0 0 16 16">
                                    <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/>
                                    <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708"/>
                                </svg>
                                &nbsp;Email já está em uso
                            `
                        span.style.color = 'red'
                        submitBtn.disabled = true
                        submitBtn.classList.add('disabled')
                        return;
                    }
                })
        } catch (error) {
            console.log(error)
        }
    })

document.querySelector('#id_password1')
    .addEventListener('input', (event) => {
        const password1 = event.target.value;
        document.querySelector('#id_password2').value = password1;
    });

