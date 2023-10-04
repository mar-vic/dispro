        var tr_override = false;

        function tr_handler(path) {
            if (!tr_override)
                window.location = path;
            else
                tr_override = false;
        }

        function cb_handler() {
            tr_override = true;
        }

        function hlTR(trid, trstate) {
            document.getElementById(trid).style.backgroundColor = trstate?"#FEF48F":"#93D2F3";
        }

        function confirmLink(theLink, text) {

            if (typeof(window.opera) != 'undefined') {  return true;  }

            var is_confirmed = confirm(text);
            if (is_confirmed) { theLink.href += '&is_js_confirmed=1'; }

            return is_confirmed;
        }

        function toggle(tid) {
            var t = document.getElementById(tid);
            t.style.display = (t.style.display == "none"?"block":"none");
        }
        function admin_toggle(tid) {
            var t = document.getElementById(tid);
            t.style.display = (t.style.display == "none"?"block":"none");
        }

        function ch_style(img, s) {
            if (s == 1) {
                img.style.border  = '2px solid #B3A585';
                img.style.margin = '0px';
            }
            else {
                img.style.border  = '0px';
                img.style.margin = '2px';
            }
        }
        document.onmousemove = captureMousePosition;
        var xdiv
        var ydiv;
        var actual_div;

        function captureMousePosition(e) {
            if (document.layers) {
                xMousePos = e.pageX;
                yMousePos = e.pageY;
            } else if (document.all) {
                xMousePos = window.event.x + document.body.scrollLeft;
                yMousePos = window.event.y + document.body.scrollTop;
            } else if (document.getElementById) {
                xMousePos = e.pageX;
                yMousePos = e.pageY;
            }
        }

        function openWindow(targ,x) {
            window.open("", targ, x, "scrollbars=no", "status=no", "menubar=no", "resizable=no") ;
        }

        function show_loginbox(alb, div) {
            if (div == 'loginbox')
                document.getElementById('album').value = alb;
            else
                xMousePos -= 200;

            document.getElementById(div).style.left = xMousePos;
            document.getElementById(div).style.top = yMousePos;
            document.getElementById(div).style.display = 'block';
            actual_div = div;

        }

        function hide_loginbox() {
            if (actual_div != '') {
                xdiv = parseInt(document.getElementById(actual_div).style.left);
                ydiv = parseInt(document.getElementById(actual_div).style.top);
                if (xMousePos < xdiv || xMousePos > xdiv+200 || yMousePos < ydiv || yMousePos > ydiv+50)
                    document.getElementById(actual_div).style.display = 'none';
            }
        }
        function SetCookie(cookieName, cookieValue, nDays) {
             var today = new Date();
             var expire = new Date();
             if (nDays==null || nDays==0) nDays=1;
             expire.setTime(today.getTime() + 3600000*24*nDays);
             document.cookie = cookieName + "=" + escape(cookieValue) + ";expires=" + expire.toGMTString();
        }
        function s_v(vr, vl) {
            document.getElementById(vr).value = vl;
            if (vr == 'dodanie')
                vypln_datumy(1);
        }
        function check_pocznak() {
        	var cislo = 250 - document.getElementById('txt').value.length;
        	document.getElementById('txt_n').value = (cislo < 0) ? 0 : cislo;
        	if ( document.getElementById('txt').value.length > 250 )  document.getElementById('txt').value = document.getElementById('txt').value.substring(0,250);
       }

       function of(nr, sx, sy){
            window.open('/obr.php?obrazok=' + nr, 'WC66', 'toolbar=no,location=no,directories=no,status=no,left=0, top=0, scrollbars=no,resizable=no,copyhistory=no,width=' + (sx + 50) + ',height=' + (sy+50));
       }
       
       function window_resize_to(){
	   	  	var oImg = document.getElementById("showImg");
	   	  	window.resizeTo((oImg.offsetWidth+50),(oImg.offsetHeight+150));
   	  }
   	  function addEvent(obj, evType, fn){
      	if (obj.addEventListener){
      		obj.addEventListener(evType, fn, false);
      		return true;
      	}
      	else if (obj.attachEvent){
      		var r = obj.attachEvent('on'+evType, fn);
      		return r;
      	}
      		else {
      		return false;
      	}
      }
       var kapitoli_typ = 2;
       function kapitoly_blind(ids,typ) {
       			if (kapitoli_typ != typ) {
       					kapitoli_typ = typ;
       					//document.getElementById('skuska').innerHTML+=kapitoli_typ+' = '+typ+'-----'+ids+'\n';
		       			var ida = ids.split(',');
		       			var i;
		       			for(i=0; i<ida.length; i++){
			       				if (typ==1) {
											document.getElementById('kapitola'+ida[i]).style.display='block';
											document.getElementById('bodky')!=undefined ? document.getElementById('bodky').style.display='none' : '';
											document.getElementById('bodky1')!=undefined ? document.getElementById('bodky1').style.display='none' : '';
											document.getElementById('zmensit')!=undefined ? document.getElementById('zmensit').style.display='block' : '';
										} else {
											document.getElementById('kapitola'+ida[i]).style.display='none';
											document.getElementById('bodky')!=undefined ? document.getElementById('bodky').style.display='block' : '';
											document.getElementById('bodky1')!=undefined ? document.getElementById('bodky1').style.display='block' : '';
											document.getElementById('zmensit')!=undefined ? document.getElementById('zmensit').style.display='none' : '';
										}
								}
						}
       }
