function validate(form_name)
{
	var text = document.getElementById("incorrect");
	var tex = new RegExp("^[^A-Z0-9a-z_]{2,15}$");
	var nom = new RegExp ("^[+0-9-]{6,11}$");
	var ema = new RegExp("[0-9a-z_]+@[0-9a-z_^.]+\\.[a-z]{2,3}");
	var Log = new RegExp("[0-9a-zA-Z]{6,20}");
	var Par = new RegExp("[0-9a-zA-Z]{6,20}");
	var Otz = new RegExp("[0-9a-zA-Z]{6,20}");
	var Otz = document.forms[form_name].Otz;
	var Fam = document.forms[form_name].secondName;
    var Im = document.forms[form_name].name;
	var email = document.forms[form_name].mail;
	var log = document.forms[form_name].login;
	var par = document.forms[form_name].password;

	if (!Otz.test(Otz.value))
	{
		Otz.style.backgroundColor="red";
        //text.style.display="block";
        Otz.focus();
        return false;
	}
	else 
	{
		document.forms[form_name].Otz.style.backgroundColor="yellow";
	}
	
	
    if (!tex.test(Fam.value))
	{ 
        Fam.style.backgroundColor="red";
        //text.style.display="block";
        Fam.focus();
        return false;
    }
    else 
	{
		document.forms[form_name].Fam.style.backgroundColor="yellow";
	}
	if (!tex.test(Im.value))
	{ 
        Im.style.backgroundColor="red";
        //text.style.display="block";
        Im.focus();
        return false;
    }
    else 
	{
		document.forms[form_name].Im.style.backgroundColor="yellow";
	}
	if (!ema.test(email.value))
	{ 
        email.style.backgroundColor="red";
        //text.style.display="block";
        email.focus();
        return false;
    }
    else 
	{
		document.forms[form_name].email.style.backgroundColor="yellow";
	}
	if (!Log.test(log.value))
	{ 
        log.style.backgroundColor="red";
        //text.style.display="block";
        log.focus();
        return false;
    }
    else 
	{
		document.forms[form_name].log.style.backgroundColor="yellow";
	}
	if (!Par.test(par.value))
	{
		par.style.backgroundColor="red";
        //text.style.display="block";
        par.focus();
        return false;
	}
	else 
	{
		document.forms[form_name].par.style.backgroundColor="yellow";
	}
	if (sog.value=="no") 
	{
		text.style.display="block";
        sog.focus();
        return false;
    }
	 else 
	 {document.forms[form_name].submit();}
}
