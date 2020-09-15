{{define "navbar"}}
  <nav class="navbar navbar-default" role="navigation">
    <div class="container-fluid">
      <div class="navbar-header">
        <a class="navbar-brand" href="/">我的博客</a>
      </div>
      <div>
        <ul class="nav navbar-nav">
          <li {{if .IsHome }} class="active" {{end}}><a href="/">首页</a></li>
          <li {{if .IsCategory }} class="active" {{end}}><a href="/category">分类</a></li>
          <li {{if .IsTopic }} class="active" {{end}}><a href="/topic">文章</a></li>
        </ul>
        <ul class="nav navbar-nav navbar-right">
          {{if .IsLogin }}
          <li>
            <a href="/login?exit=true">退出</a>
          </li>
          {{else}}
          <li>
            <a href="/login">登录</a>
          </li>
          {{end}}
        </ul>
      </div>
    </div>
  </nav>
{{end}}