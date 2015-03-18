#!/usr/bin/ruby

require 'rubygems'
require 'mechanize'
require 'json'
require 'ruby-debug'

stop_words = {}
File.open("stopwords", "r") do |f|
	stop_words = JSON.load(f)
end


filename = "suicide_project_results_1"
word_count_hash = {}
res = {}

Dir["scraped_data/*"].each do |f|
	File.open(f, "r") do |fin|
		res = JSON.load(fin)
		res.each do |url,comments|
			arr = comments['source'].split(/\s|\./)
			arr.each do |word|
				word = word.gsub(/,|\-|\"/,'').downcase
				unless stop_words.has_key?(word)
					if word_count_hash.has_key?(word)
						word_count_hash[word] += 1
					else
						word_count_hash[word] = 1
					end
				end
			end
		end
	end
end

sorted_list =word_count_hash.sort_by{|k,v| v}

word_limit = 200
c = 0

fo = File.open("sorted_word_list", "w")

sorted_list.reverse.each do |arr|
	fo << "#{arr[0]}\t=>#{arr[1]}\n"
	c = c+1
	if c > word_limit
		fo.close
		puts 'end of program'
		exit
	end
end


