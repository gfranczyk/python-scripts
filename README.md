As the description suggests - this is (or will be) a collection of various standalone Python scripts \ projects.

Some will be abstracted to the point they can be used directly for different implements; however, many \ most will be tailored to particular use cases (of varying specificity) and will require some tweaks to get set up for a different use case.  I've figured it's better to share more than the converse, at minimum some of these will be good starting points for future projects.

Projects so far:

* log-recorder: simple script for tailing apache logs (using a specific log format) to create a list of URL's.  
	** Original Use Case: List of production URL's to replay for DR cache warming \ production load testing.  
	** Usuage Info: log_recorder.py [working directory, Default: /tmp] [log directory, Default: /var/log/apache/] [hostname \ url prefex, Default: http://www.default.com]  
			Currently looks for the URL after the first quote quote in the line, after the Request Method (line 17).  
			Once the log recorder is started it runs perpetually until interrupted \ killed.     
		
