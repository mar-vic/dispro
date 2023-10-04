var stormCookie = {
    /**
     * Read and get cookie
     *
     * @param {string} name
     *
     * @returns {string|null}
     */
    getCookie: function(name) {
        var nameEq  = name + "=";
        var data    = document.cookie.split(';');
        for(var i=0; i < data.length; i++) {
            var dataPart = data[i];
            while (dataPart.charAt(0) == ' ') {
                dataPart = dataPart.substring(1, dataPart.length);
            }
            if (dataPart.indexOf(nameEq) == 0) {
                return unescape(dataPart.substring(nameEq.length, dataPart.length));
            }
        }
        return null;
    },
    /**
     * Create cookie
     *
     * @param {string} name
     * @param {string} value
     * @param {number} ttlInSeconds
     * @param {string} domain
     * @param {string} path
     */
    addCookie: function(name, value, ttlInSeconds, domain, path) {
        var expires = '';
        if (ttlInSeconds) {
            var date = new Date();
            date.setTime(date.getTime()+(ttlInSeconds*1000));
            expires = '; expires='+date.toGMTString();
        }
        domain = (domain) ? ';domain=' + domain : '';
        path = (path) ? ';path=' + path : '';
        document.cookie = name+'='+value+path+domain+expires;
    },
    /**
     * Remove cookie
     *
     * @param {string} name
     * @param {string} domain
     * @param {string} path
     */
    removeCookie: function(name, domain, path) {
        this.addCookie(name, '', -1, domain, path);
    }
};