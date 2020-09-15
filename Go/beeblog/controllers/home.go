package controllers

import (
	"beeblog/models"

	"github.com/astaxie/beego"
)

// HomeController class
type HomeController struct {
	beego.Controller
}

// Get method for REST
func (c *HomeController) Get() {
	// c.Data["Website"] = "beego.me"
	// c.Data["Email"] = "astaxie@gmail.com"
	c.TplName = "home.html"
	c.Data["Title"] = "首页"
	c.Data["IsHome"] = true
	retVal := checkAccount(c.Ctx)
	c.Data["IsLogin"] = retVal
	cate := c.Input().Get("cate")
	topics, err := models.GetAllTopics(cate, true)
	if err != nil {
		beego.Error(err.Error())
		return
	}
	c.Data["Topics"] = topics
	var categories []*models.Category
	categories, err = models.GetAllCategories()
	if err != nil {
		beego.Error(err)
	}
	c.Data["Categories"] = categories
}
