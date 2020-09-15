package controllers

import (
	"beeblog/models"

	"github.com/astaxie/beego"
)

// TopicController class
type TopicController struct {
	beego.Controller
}

// Get method for REST
func (c *TopicController) Get() {
	c.TplName = "topic.html"
	c.Data["Title"] = "文章"
	c.Data["IsTopic"] = true
	c.Data["IsLogin"] = checkAccount(c.Ctx)
	topics, err := models.GetAllTopics("", false)
	if err != nil {
		beego.Error(err.Error())
		return
	}
	c.Data["Topics"] = topics
}

// Add method for REST
func (c *TopicController) Add() {
	c.TplName = "topic_add.html"
	c.Data["Title"] = "添加文章"
	c.Data["IsTopic"] = true
	c.Data["IsLogin"] = checkAccount(c.Ctx)
}

// Post method for REST
func (c *TopicController) Post() {
	if !checkAccount(c.Ctx) {
		c.Redirect("/login", 302)
		return
	}
	title := c.Input().Get("title")
	content := c.Input().Get("content")
	category := c.Input().Get("category")
	id := c.Input().Get("tID")
	var err error
	if len(id) == 0 {
		err = models.AddTopic(title, category, content)
	} else {
		err = models.ModifyTopic(id, title, category, content)
	}
	if err != nil {
		beego.Error(err)
	}
	c.Redirect("/topic", 302)
}

// View method
func (c *TopicController) View() {
	c.TplName = "topic_view.html"
	c.Data["IsTopic"] = true
	c.Data["IsLogin"] = checkAccount(c.Ctx)
	tid := c.Ctx.Input.Param("0")
	topic, err := models.GetTopic(tid)
	if err != nil {
		beego.Error(err.Error())
		c.Redirect("/", 302)
		return
	}
	c.Data["Title"] = topic.Title
	c.Data["Topic"] = topic
	c.Data["TID"] = tid

	var replies []*models.Comment
	replies, err = models.GetAllReplies(tid)
	c.Data["Replies"] = replies
}

// Modify method
func (c *TopicController) Modify() {
	c.TplName = "topic_modify.html"
	c.Data["IsTopic"] = true
	c.Data["IsLogin"] = checkAccount(c.Ctx)
	id := c.Input().Get("id")
	topic, err := models.GetTopic(id)
	if err != nil {
		beego.Error(err.Error())
		c.Redirect("/", 302)
		return
	}
	c.Data["Title"] = topic.Title
	c.Data["Topic"] = topic
	c.Data["TID"] = id
}

// Delete method
func (c *TopicController) Delete() {
	if !checkAccount(c.Ctx) {
		c.Redirect("/login", 302)
		return
	}
	topicID := c.Input().Get("id")
	if len(topicID) == 0 {
	}
	err := models.DeleteTopic(topicID)
	if err != nil {
		beego.Error(err)
	}
	c.Redirect("/topic", 302)
	return
}
