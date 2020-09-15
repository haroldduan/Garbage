package controllers

import (
	"github.com/astaxie/beego"
	"github.com/astaxie/beego/context"
)

// LoginController class
type LoginController struct {
	beego.Controller
}

// Get method for REST
func (c *LoginController) Get() {
	exit := c.Input().Get("exit") == "true"
	if exit {
		c.Ctx.SetCookie("username", "", -1, "/")
		c.Ctx.SetCookie("password", "", -1, "/")
		c.Redirect("/", 302)
		return
	}
	c.TplName = "login.html"
	c.Data["Title"] = "登录"
}

// Post method for REST
func (c *LoginController) Post() {
	userName := c.Input().Get("userName")
	password := c.Input().Get("password")
	autoLogin := c.Input().Get("autoLogin") == "on"

	if beego.AppConfig.String("username") == userName &&
		beego.AppConfig.String("password") == password {
		maxAge := 0
		if autoLogin {
			maxAge = 1<<31 - 1
		}
		c.Ctx.SetCookie("username", userName, maxAge, "/")
		c.Ctx.SetCookie("password", password, maxAge, "/")
	}
	c.Redirect("/", 302)
	return
}

// checkAccount method
func checkAccount(ctx *context.Context) bool {
	ck, err := ctx.Request.Cookie("username")
	if err != nil {
		return false
	}
	userName := ck.Value
	ck, err = ctx.Request.Cookie("password")
	if err != nil {
		return false
	}
	password := ck.Value

	return beego.AppConfig.String("username") == userName &&
		beego.AppConfig.String("password") == password
}
