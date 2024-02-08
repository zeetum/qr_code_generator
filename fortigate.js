<script>
// Example URL (note that Username is the only variable):
// sig.site.internal:1000/login?#Username
function prefillUsername(){
    var hash = '#' + location.hash.replace('#', '');
    document.getElementById("ft_un").value = hash.substring(1)
}

document.addEventListener("DOMContentLoaded", prefillUsername);
</script>
