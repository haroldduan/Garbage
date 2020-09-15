package models

import (
	"os"
	"path"
	"strconv"
	"time"

	"github.com/astaxie/beego/orm"

	// sqlite3 drivers
	_ "github.com/mattn/go-sqlite3"
	"github.com/unknwon/com"
)

const (
	//DbName database name
	DbName = "data/beeblog.db"
	//Sqlite3Driver sqlite driver
	Sqlite3Driver = "sqlite3"
)

// Category class
type Category struct {
	ID              int64 `orm:"column(id)"`
	Title           string
	Created         time.Time `orm:"index"`
	Views           int64     `orm:"index"`
	TopicTime       time.Time
	TopicCount      int64
	TopicLastUserID int64 `orm:"column(topic_last_user_id)"`
}

// Topic class
type Topic struct {
	ID              int64 `orm:"column(id)"`
	UserID          int64 `orm:"column(user_id)"`
	Title           string
	Category        string
	Content         string `orm:"size(5000)"`
	Attachment      string
	Created         time.Time `orm:"index"`
	Updated         time.Time `orm:"index"`
	Views           int64     `orm:"index"`
	Author          string
	ReplyTime       time.Time
	ReplyCount      int64
	ReplyLastUserID int64 `orm:"column(reply_last_user_id);index"`
}

// Comment class
type Comment struct {
	ID      int64 `orm:"column(id)"`
	TopicID int64 `orm:"column(topic_id)"`
	Name    string
	Content string    `orm:"size(1000)"`
	Created time.Time `orm:"index"`
}

// RegisterDB method
func RegisterDB() {
	if !com.IsExist(DbName) {
		os.MkdirAll(path.Dir(DbName), os.ModePerm)
		os.Create(DbName)
	}
	orm.RegisterModel(new(Category), new(Topic), new(Comment))
	orm.RegisterDriver(Sqlite3Driver, orm.DRSqlite)
	orm.RegisterDataBase("default", Sqlite3Driver, DbName, 10)
}

// AddCategory method
func AddCategory(name string) error {
	o := orm.NewOrm()
	category := &Category{
		Title:           name,
		Created:         time.Now(),
		Views:           0,
		TopicTime:       time.Now(),
		TopicCount:      0,
		TopicLastUserID: 1,
	}
	qs := o.QueryTable("category")
	err := qs.Filter("title", name).One(category)
	if err == nil {
		return err
	}
	_, err = o.Insert(category)
	if err != nil {
		return err
	}
	return nil
}

// GetAllCategories method
func GetAllCategories() ([]*Category, error) {
	o := orm.NewOrm()
	categories := make([]*Category, 0)
	qs := o.QueryTable("category")
	_, err := qs.All(&categories)
	return categories, err
}

// DeleteCategory method
func DeleteCategory(id string) error {
	cID, err := strconv.ParseInt(id, 10, 64)
	if err != nil {
		return err
	}
	o := orm.NewOrm()
	category := &Category{ID: cID}
	_, err = o.Delete(category)
	return err
}

// AddTopic method
func AddTopic(title, category, content string) error {
	o := orm.NewOrm()
	topic := &Topic{
		UserID:          1,
		Title:           title,
		Category:        category,
		Content:         content,
		Attachment:      "",
		Created:         time.Now(),
		Updated:         time.Now(),
		Views:           0,
		Author:          "",
		ReplyTime:       time.Now(),
		ReplyCount:      0,
		ReplyLastUserID: 999,
	}
	_, err := o.Insert(topic)
	if err != nil {
		return err
	}
	cate := &Category{}
	qs := o.QueryTable("Category")
	err = qs.Filter("title", category).One(cate)
	if err == nil {
		cate.TopicCount++
		_, err = o.Update(cate)
	}
	return err
}

// GetAllTopics method
func GetAllTopics(cate string, isDesc bool) ([]*Topic, error) {
	o := orm.NewOrm()
	topics := make([]*Topic, 0)
	qs := o.QueryTable("topic")
	var err error
	if len(cate) > 0 {
		qs = qs.Filter("category", cate)
	}
	if isDesc {
		_, err = qs.OrderBy("-created").All(&topics)
	} else {
		_, err = qs.All(&topics)
	}
	return topics, err
}

// GetTopic method
func GetTopic(id string) (*Topic, error) {
	idNum, err := strconv.ParseInt(id, 10, 64)
	if err != nil {
		return nil, err
	}
	o := orm.NewOrm()
	topic := &Topic{}
	qs := o.QueryTable("topic")
	err = qs.Filter("id", idNum).One(topic)
	if err != nil {
		return nil, err
	}
	topic.Views++
	_, err = o.Update(topic)
	return topic, err
}

// ModifyTopic method
func ModifyTopic(id, title, category, content string) error {
	idNum, err := strconv.ParseInt(id, 10, 64)
	if err != nil {
		return err
	}
	var oldCate string
	o := orm.NewOrm()
	topic := &Topic{ID: idNum}
	if o.Read(topic) == nil {
		oldCate = topic.Category
		topic.Title = title
		topic.Category = category
		topic.Content = content
		topic.Updated = time.Now()
		_, err = o.Update(topic)
		if err != nil {
			return err
		}
	}
	// 更新分类统计
	if len(oldCate) > 0 {
		cate := new(Category)
		qs := o.QueryTable("category")
		err = qs.Filter("title", oldCate).One(cate)
		if err == nil {
			cate.TopicCount--
			_, err = o.Update(cate)
		}
	}
	cate := new(Category)
	qs := o.QueryTable("category")
	err = qs.Filter("title", category).One(cate)
	if err == nil {
		cate.TopicCount++
		_, err = o.Update(cate)
	}
	return err
}

// DeleteTopic method
func DeleteTopic(id string) error {
	tID, err := strconv.ParseInt(id, 10, 64)
	if err != nil {
		return err
	}
	o := orm.NewOrm()
	topic := &Topic{ID: tID}
	_, err = o.Delete(topic)
	return err
}

// AddReply method
func AddReply(tid, nickname, content string) error {
	tID, err := strconv.ParseInt(tid, 10, 64)
	if err != nil {
		return err
	}
	o := orm.NewOrm()
	comment := &Comment{
		TopicID: tID,
		Name:    nickname,
		Content: content,
		Created: time.Now(),
	}
	_, err = o.Insert(comment)
	return err
}

// GetAllReplies method
func GetAllReplies(tid string) ([]*Comment, error) {
	tID, err := strconv.ParseInt(tid, 10, 64)
	if err != nil {
		return nil, err
	}
	o := orm.NewOrm()
	comments := make([]*Comment, 0)
	qs := o.QueryTable("comment")
	_, err = qs.Filter("topic_id", tID).All(&comments)
	return comments, err
}

// DeleteReply method
func DeleteReply(rid string) error {
	ridNum, err := strconv.ParseInt(rid, 10, 64)
	if err != nil {
		return err
	}
	o := orm.NewOrm()
	comment := &Comment{ID: ridNum}
	_, err = o.Delete(comment)
	return err
}
