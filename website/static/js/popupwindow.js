const PopUp = {
    init(){
        this.el = document.createElement('div')
        
        this.el.className = 'popup-window'
        document.body.appendChild(this.el)
    },
    show(insideStructure){
        this.el.innerHTML = insideStructure
        this.el.className = 'popup-visible'

    },
    hide(){
        this.el.classList.remove('popup-visible')
        this.el.innerHTML = '' 
    }
}