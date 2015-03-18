#!/usr/bin/ruby

require 'rubygems'
require 'mechanize'
require 'json'
require 'ruby-debug'

pg_no = 1#2007
stop_when = 3
data_file = "suicide_project_results_#{pg_no}"
seed_url = "http://suicideproject.org/page/"

agent = Mechanize.new

def collect_dicussion_links(tags)
	l = []
	tags.each do |t|
		l << t['href']
	end
	return l
end

def load_data(filename)
	begin
		File.open(filename, "r") do |f|
			res = JSON.load(f)
		end
	rescue
		puts "Failed to read the file"
		res = {}
	end
end

h = load_data(data_file) || {}
must_write_to_file = false

#=begin
begin

	while true
		url = seed_url + pg_no.to_s
		puts "Scraping page and its decendents with URL"
		puts "=========================================\n#{url}"

		pg = agent.get(url)
		tags = pg.search("h2 > a")

		collect_dicussion_links(tags).each do |dl|
			puts dl
			# Some of the very old links longer exist
			if (dl =~ /200\d\/\d+\/\d+/)
				next
			end

			if !h.has_key?(dl)
				must_write_to_file = true

				pg = agent.get(dl)
				main = pg.search("div.entrytext p")
				h[dl] = {'source' => main[0...-1].text}

				comments = []
				pg.search("div.rule").each do |comment|
					comments << comment.search("p").text
				end
				h[dl]['replies'] = comments
				sleep(2) # be polite; don't jam their website
			else
				puts "Scraped before! => #{dl}"
			end

		end

		pg_no = pg_no + 1
#=begin
		if pg_no > stop_when
			exit
		end
#=end
	end
rescue Mechanize::ResponseCodeError => e
	puts "Reponse code error: " + e	# aka End of Scraping
ensure
	puts "Rewrite file => #{must_write_to_file}"

	if must_write_to_file
		fo = File.new(data_file, "w")
		puts "Updating the data file"
		fo << JSON.dump(h)
		fo.close()
	end

end
#=end
