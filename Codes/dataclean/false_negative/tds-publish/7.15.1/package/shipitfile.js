module.exports = (shipit) => {
  require("shipit-deploy")(shipit);

  shipit.initConfig({
    default: {
      workspace: process.env.WORKSPACE,
      deployTo: process.env.DEPLOY_PATH,
      repositoryUrl: process.env.REPO_URL,
      ignores: [".git", "node_modules"],
      keepReleases: 2,
      keepWorkspace: false, // should we remove workspace dir after deploy?
      deleteOnRollback: false,
      key: process.env.KEY_PATH,
      shallowClone: true,
      deploy: {
        remoteCopy: {
          copyAsDir: false, // Should we copy as the dir (true) or the content of the dir (false)
        },
      },
    },
    production: {
      servers: process.env.DEPLOY_SERVER,
    },
  });
};
