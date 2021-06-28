function openForm(id)
{
  id.style.display = "flex";
}

function exit(id)
{
    id.style.display = "none";
}

//If the user has mobility impairments, this allows them to exit the registration form using the escape button
document.addEventListener('keydown', function(input) {
  if(input.key === "Escape"){
    document.getElementById('bookclubrego').style.display = "none";
  }
});