const Toast = {
    init(){
        this.hideTimeout = null




        this.el = document.createElement('div')
        this.el.className = 'toast';
        document.body.appendChild(this.el)

    },
    show(message,state,timeForAppear=2000){
        clearTimeout(this.hideTimeout)
        this.el.textContent = message
        this.el.className = 'toast toast-visible'
        if(state){
            var newState = state == "S" ? "toast-success" : "toast-error"
            this.el.classList.add(newState)
        }
        this.hideTimeout = setTimeout(() => {
            this.el.classList.remove('toast-visible')
        },timeForAppear)
    }

};



document.addEventListener('DOMContentLoaded', () => Toast.init())


