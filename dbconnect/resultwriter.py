from abc import ABC, abstractmethod

class QueryResultWriter(ABC):
	@abstractmethod
	def write(self, query_result):
		pass

class VerboseQueryResultWriter(QueryResultWriter):
	def write(self, query_result):
		builder = []
		# output is ignored for console printer

		builder.append("======================================")

		if hasattr(query_result.query, "name"):
			builder.append("Name: %s" % query_result.query.name)

		builder.append("SQL: %s" % query_result.query.sql)
		builder.append("Params: %s" % query_result.query.params)
		builder.append("Compiled SQL: %s" % query_result.query.compiled_sql)
		builder.append("Ran for: %s" % query_result.format_time())
		builder.append("Row count: %s" % query_result.rowcount)

		if query_result.rows is not None and len(query_result.rows) > 0:
			builder.append("--------------------------------------")
			builder.append("Rows: ")
			builder.append("--------------------------------------")

			query_result.forEach(lambda r: builder.append(str(r)))

		builder.append(" ")
		return "\n".join(builder)

class ConciseQueryResultWriter(QueryResultWriter):
	def write(self, query_result):
		if hasattr(query_result.query, "name"):
			params = {
				"name": query_result.query.name,
				"rowcount": query_result.rowcount,
				"runtime": query_result.format_time()
			}
			return "%(name)s = %(rowcount)s (%(runtime)s)" % params

		params = {"rowcount": query_result.rowcount, "runtime": query_result.format_time()}
		return "[%(rowcount)s (%(runtime)s)]\n" % params