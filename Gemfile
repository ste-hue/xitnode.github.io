source "https://rubygems.org"

# Jekyll core (was previously pulled in by the github-pages gem)
gem "jekyll", "~> 4.4"
gem "minima", "~> 2.5"

# Stdlib gems no longer bundled with Ruby 3.4+ / 4.x
gem "csv"
gem "base64"
gem "bigdecimal"
gem "logger"
gem "webrick"

# Jekyll plugins
group :jekyll_plugins do
  gem "jekyll-feed"
  gem "jekyll-sitemap"
  gem "jekyll-seo-tag"
end

# Windows and JRuby do not include zoneinfo files, so bundle the tzinfo-data gem
# and associated library.
platforms :mingw, :x64_mingw, :mswin, :jruby do
  gem "tzinfo", ">= 1", "< 3"
  gem "tzinfo-data"
end

# Performance-booster for watching directories on Windows
gem "wdm", "~> 0.1.1", :platforms => [:mingw, :x64_mingw, :mswin]

# Lock `http_parser.rb` gem to `v0.6.x` on JRuby builds since newer versions of the gem
# do not have a Java counterpart.
gem "http_parser.rb", "~> 0.6.0", :platforms => [:jruby]
