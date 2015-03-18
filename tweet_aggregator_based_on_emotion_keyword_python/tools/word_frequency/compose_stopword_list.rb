require 'rubygems'
require 'json'
require 'csv'
require 'ruby-debug'

stopwords = {}
counter = 0
File.open("./stopwords/csv_stopwords.txt", "r") do |infile|
    while (line = infile.gets)
	csv_arr = line.split(",")
	counter = csv_arr.size
	csv_arr.each do |w|
		stopwords[w.strip] = 1
	end
    end
end

puts counter

File.open("./stopwords/newline_stopwords.txt", "r") do |infile|
    while (line = infile.gets)
	if line.strip =~ /.+/
		stopwords[line.strip] = 1
	        counter = counter + 1
	end
    end
end


pp stopwords
puts counter


File.open("./stopwords/stopwords", 'w') do |f|
	f.write(stopwords.to_json)
end

puts 'end of program'

