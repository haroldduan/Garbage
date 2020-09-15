package controllers

import (
	"beeblog/models"

	"github.com/astaxie/beego"
)

// CategoryController class
type CategoryController struct {
	beego.Controller
}

// Get method for REST
func (c *CategoryController) Get() {
	op := c.Input().Get("op")
	switch op {
	case "add":
		categoryName := c.Input().Get("categoryName")
		if len(categoryName) == 0 {
			break
		}
		err := models.AddCategory(categoryName)
		if err != nil {
			beego.Error(err)
		}
		c.Redirect("/category", 302)
		return
	case "del":
		categoryID := c.Input().Get("id")
		if len(categoryID) == 0 {
			break
		}
		err := models.DeleteCategory(categoryID)
		if err != nil {
			beego.Error(err)
		}
		c.Redirect("/category", 302)
		return
	}
	c.TplName = "category.html"
	c.Data["Title"] = "分类"
	c.Data["IsCategory"] = true

	var err error
	c.Data["Categories"], err = models.GetAllCategories()
	if err != nil {
		beego.Error(err)
	}
}
