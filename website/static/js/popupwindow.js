const PopUp = {
    init(){
        this.el = document.createElement('div')
        this.subelem = document.createElement('div')
        this.subelem.className = 'centered'
        this.el.className = 'popup-window'
        this.el.appendChild(this.subelem)
        document.body.appendChild(this.el)
        
    },
    show(insideStructure){
        
        this.el.className = 'popup-window popup-visible'
        this.subelem.innerHTML = insideStructure

    },
    hide(){
        this.el.classList.remove('popup-visible')
        
    }
}

document.addEventListener('DOMContentLoaded', () => PopUp.init())



