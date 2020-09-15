package controllers

import (
	"beeblog/models"

	"github.com/astaxie/beego"
)

// ReplyController class
type ReplyController struct {
	beego.Controller
}

// Add method
func (c *ReplyController) Add() {
	tid := c.Input().Get("tid")
	err := models.AddReply(tid,
		c.Input().Get("nickname"),
		c.Input().Get("content"),
	)
	if err != nil {
		beego.Error(err.Error())
	}
	c.Redirect("/topic/view/"+tid, 302)
}

// Delete method
func (c *ReplyController) Delete() {
	tid := c.Input().Get("tid")
	rid := c.Input().Get("rid")
	err := models.DeleteReply(rid)
	if err != nil {
		beego.Error(err.Error())
	}
	c.Redirect("/topic/view/"+tid, 302)
}
