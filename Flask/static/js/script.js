// JavaScript to toggle sections
function showSection(id) {
    var sections = document.querySelectorAll("section");
    sections.forEach(section => section.classList.remove("active"));
    document.getElementById(id).classList.add("active");
}


// Open modal
function openModal(id){
  document.getElementById(id).style.display = 'block';
}

// Close modal
function closeModal(id){
  document.getElementById(id).style.display = 'none';
}

// Close modal if user clicks outside content
window.onclick = function(event){
  ['inc','xcep','res','vgg'].forEach(function(id){
    var modal = document.getElementById(id);
    if(event.target == modal){
      modal.style.display = 'none';
    }
  });
}
