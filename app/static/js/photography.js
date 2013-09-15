$(window).load(function() {
var container = document.querySelector('#horizontal-grid-packing')
var imagesHTML = container.innerHTML
var pack = Pack(container, {
  padding:0 
})
window.addEventListener('resize', function () {
  pack.width = container.clientWidth
  pack.height = Math.round(window.innerHeight / Math.PI)
  pack.reload()
})
function append() {
  var frag = document.createElement('div')
  frag.innerHTML = imagesHTML
  pack.append(frag.children)
}
});
