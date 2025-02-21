const slug = document.querySelector("meta[name='user-slug']").getAttribute('content');
const loader = document.querySelector('#loader')

document.addEventListener('DOMContentLoaded', function () {
    loader.style.display = "none"
});
