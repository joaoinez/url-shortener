require("conform").formatters.prettierd = {
	append_args = function()
		return { "--config", "prettier.config.js" }
	end,
}
